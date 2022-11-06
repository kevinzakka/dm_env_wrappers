"""A wrapper for logging to Weights & Biases."""

from typing import Any, Callable, Dict, Optional, Union

import dm_env
import numpy as np

from dm_env_wrappers._src import base

FnType = Callable[[Any], Dict[str, Union[float, np.ndarray]]]

# This will contain all functions decorated with `wblog` even if the environment is not
# using wrappers that call the decorator.
_ALL_DECORATED: Dict[str, Any] = {}


def wblog(func: Callable) -> Callable:
    """A decorator for logging functions to Weights & Biases.

    This decorator will log the return value of the function to Weights & Biases when
    `.log()` is called. The return value must be a dictionary of key-value pairs,
    where the keys are strings and the values are scalars or numpy arrays.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.
    """
    _ALL_DECORATED[func.__name__] = func
    return func


class WandbLoggerWrapper(base.EnvironmentWrapper):
    """Logs any environment methods decorated with @wblog to Weights & Biases.

    This wrapper will find all functions decorated with @wblog and log their return
    values to Weights & Biases when `.log()` is called. Any function decorated with
    @wblog must return a dictionary of key-value pairs, where they keys are strings
    and the values are scalars or numpy arrays.
    """

    def __init__(
        self,
        environment: dm_env.Environment,
        wandb_run: Any,
        prefix: Optional[str] = None,
    ) -> None:
        """Initializes the wrapper.

        Args:
            environment: The environment to wrap.
            wandb_run: The Weights & Biases run object.
            prefix: A prefix to add to all logged keys. The final key will be of the
                form "{prefix}/{key}".
        """
        super().__init__(environment)

        self._wandb_run = wandb_run
        self._prefix = prefix

        # Only grab decorated functions that are defined in the environment's class,
        # i.e., in `self._environment`.
        self._registry: Dict[str, FnType] = {}
        for name, func in _ALL_DECORATED.items():
            if hasattr(self._environment, name):
                self._registry[name] = func

    def log(self, step: int) -> None:
        """Logs all @wblogged functions to Weights & Biases.

        Args:
            step: The current step.
        """
        # It's cheaper to call wandb.log once with a dictionary than to call it
        # multiple times with a single key-value pair.
        log_dict = {}
        for name, func in self._registry.items():
            ret = func(self)
            self._check_decorated_return(name, ret)
            for k, v in ret.items():
                if self._prefix:
                    k = f"{self._prefix}/{k}"
                log_dict[k] = v
        self._wandb_run.log(log_dict, step=step)

    def _check_decorated_return(self, name: str, ret: Any) -> None:
        # The return type must be a dictionary.
        if not isinstance(ret, dict):
            raise ValueError(f"Return value of {name} must be a dictionary.")
        # All keys must be strings.
        if not all(isinstance(k, str) for k in ret.keys()):
            raise ValueError(f"All keys of {name} must be strings.")
        # Each value must be a scalar or numpy array.
        if not all(isinstance(v, (float, np.ndarray)) for v in ret.values()):
            raise ValueError(f"All values of {name} must be scalars or numpy arrays.")
