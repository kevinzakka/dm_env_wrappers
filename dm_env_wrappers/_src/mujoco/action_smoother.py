"""A wrapper for smoothing actions via filtering.

Adapted from https://github.com/erwincoumans/motion_imitation.
"""

import enum
from collections import deque
from typing import Deque, Optional, Sequence, Union

import dm_env
import numpy as np
from dm_env_wrappers._src import base
from scipy.signal import butter

# Default filter order.
_FILTER_ORDER = 2

# Default lowcut and highcut frequencies, in Hz.
_FILTER_LOWCUT = 0.0
_FILTER_HIGHCUT = 4.0


class _FilterType(enum.Enum):
    """Allowed filter types."""

    LOW_PASS = 0
    BAND_PASS = 1


class _Filter:
    """A generic low-pass or band-pass filter."""

    def __init__(
        self,
        a: np.ndarray,
        b: np.ndarray,
        order: int,
        filter_type: _FilterType,
    ) -> None:
        self._a = a
        self._b = b

        # Normalize the filter coefficients.
        for i in range(len(self._a)):
            self._b[i] /= self._a[i][0]
            self._a[i] /= self._a[i][0]

        self._dim = a.shape[0]
        if filter_type == _FilterType.LOW_PASS:
            assert len(self._b[0]) == len(self._a[0]) == order + 1
            self._hist_len = order
        elif filter_type == _FilterType.BAND_PASS:
            assert len(self._b[0]) == len(self._a[0]) == 2 * order + 1
            self._hist_len = 2 * order
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")

        self._yhist: Deque[np.ndarray] = deque(maxlen=self._hist_len)
        self._xhist: Deque[np.ndarray] = deque(maxlen=self._hist_len)
        self.reset()

    def reset(self) -> None:
        """Reset the filter's history."""
        self._yhist.clear()
        self._xhist.clear()
        for _ in range(self._hist_len):
            self._yhist.appendleft(np.zeros((self._dim, 1)))
            self._xhist.appendleft(np.zeros((self._dim, 1)))

    def init_history(self, x: np.ndarray) -> None:
        """Initialize the filter's history."""
        for i in range(self._hist_len):
            self._xhist[i] = x[..., None]
            self._yhist[i] = x[..., None]

    def __call__(self, x: np.ndarray) -> np.ndarray:
        xs = np.concatenate(list(self._xhist), axis=-1)
        ys = np.concatenate(list(self._yhist), axis=-1)
        y = (
            np.multiply(x, self._b[:, 0])
            + np.sum(np.multiply(xs, self._b[:, 1:]), axis=-1)
            - np.sum(np.multiply(ys, self._a[:, 1:]), axis=-1)
        )
        self._xhist.appendleft(x[..., None].copy())
        self._yhist.appendleft(y[..., None].copy())
        return y


class ButterworthFilter(_Filter):
    """A Butterworth low-pass or band-pass filter.

    Args:
        lowcut: A list of lowcut frequencies, in Hz. If all values are 0, then a
            low-pass filter is used, otherwise a band-pass filter is used. No mixture
            of 0 and non-zero values is allowed.
        highcut: A list of highcut frequencies, in Hz.
        sampling_rate: The sampling rate of the signal, in Hz.
        order: The order of the filter.
    """

    def __init__(
        self,
        lowcut: Sequence[float],
        highcut: Sequence[float],
        sampling_rate: float,
        order: int,
    ) -> None:
        low = np.asarray(lowcut)
        high = np.asarray(highcut)

        if len(low) != len(high):
            raise ValueError(
                "The number of lowcut and highcut frequencies must be the same."
            )
        if np.any(low == 0.0) and np.any(low > 0.0):
            raise ValueError(
                "All filter dimensions must be either low-pass or band-pass."
            )
        if np.any(high <= 0.0):
            raise ValueError("Highcut frequencies must be strictly positive.")
        if np.any(low < 0.0):
            raise ValueError("Lowcut frequencies must be non-negative.")

        if np.any(lowcut):
            filter_type = _FilterType.BAND_PASS
        else:
            filter_type = _FilterType.LOW_PASS

        a_coefs = []
        b_coefs = []
        for lo, hi in zip(low, high):
            b, a = self._get_filter_coefficients(lo, hi, sampling_rate, order)
            a_coefs.append(a)
            b_coefs.append(b)

        a = np.stack(a_coefs)
        b = np.stack(b_coefs)
        super().__init__(a, b, order, filter_type)

    def _get_filter_coefficients(
        self,
        lowcut: float,
        highcut: float,
        sampling_rate: float,
        order: int,
    ):
        nyq = 0.5 * sampling_rate
        low = lowcut / nyq
        high = highcut / nyq
        # NOTE(kevin): This returns a tuple of (b, a) coefficients.
        if low > 0:
            return butter(order, [low, high], btype="band")
        return butter(order, high, btype="low")


class ActionSmootherWrapper(base.EnvironmentWrapper):
    """Digitally filter the actions to smooth them out.

    This is useful for stochastic policies, where the actions are sampled from a
    distribution like a Gaussian.

    Args:
        environment: The environment to wrap.
        lowcut: The lowcut frequency of the filter. Can be a single value which means
            that the same lowcut is used for all action dimensions. Otherwise, a
            list of values can be provided, one for each action dimension. If None,
            then a low-pass filter is used, otherwise a band-pass filter is used.
        highcut: The highcut frequency of the filter. Can be a single value which means
            that the same highcut is used for all action dimensions. Otherwise, a
            list of values can be provided, one for each action dimension.
        order: The order of the filter.
    """

    def __init__(
        self,
        environment: dm_env.Environment,
        highcut: Optional[Union[float, Sequence[float]]] = None,
        lowcut: Optional[Union[float, Sequence[float]]] = None,
        order: int = _FILTER_ORDER,
    ) -> None:
        super().__init__(environment)

        action_spec = self._environment.action_spec()
        self._action_dim = action_spec.shape[0]
        self._action_dtype = action_spec.dtype

        # Set the default pose to be the midpoint of the action space.
        self._default_action = (action_spec.maximum + action_spec.minimum) / 2.0

        # Get the control frequency.
        control_frequency = 1.0 / self._environment.control_timestep()

        low = _set_default_or_expand(lowcut, _FILTER_LOWCUT, self._action_dim, "lowcut")
        high = _set_default_or_expand(
            highcut, _FILTER_HIGHCUT, self._action_dim, "highcut"
        )
        self._filter = ButterworthFilter(
            lowcut=low,
            highcut=high,
            sampling_rate=control_frequency,
            order=order,
        )

    def step(self, action) -> dm_env.TimeStep:
        filtered_action = self._filter(action).astype(self._action_dtype)
        return self._environment.step(filtered_action)

    def reset(self) -> dm_env.TimeStep:
        self._filter.reset()
        self._filter.init_history(self._default_action)
        return self._environment.reset()


def _set_default_or_expand(
    value: Optional[Union[float, Sequence[float]]],
    default: float,
    length: int,
    name: str,
) -> Sequence[float]:
    if value is None:
        return [default] * length
    if isinstance(value, (float, int)):
        return [float(value)] * length
    if len(value) != length:
        raise ValueError(f"{name} must be a list of length {length}, but got {value}.")
    return value
