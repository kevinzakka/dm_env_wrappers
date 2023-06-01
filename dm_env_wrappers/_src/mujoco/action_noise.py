# Copyright 2018 The dm_control Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or  implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Wrapper that adds zero-mean Gaussian noise to the actions.

Adapted from https://github.com/deepmind/dm_control/blob/main/dm_control/suite/wrappers/action_noise.py.
"""

from typing import Optional

import dm_env

from dm_env_wrappers._src import base
import numpy as np

_BOUNDS_MUST_BE_FINITE = (
    "All bounds in `env.action_spec()` must be finite, got: {action_spec}"
)


class ActionNoiseWrapper(base.EnvironmentWrapper):
    """A wrapper that adds zero-mean Gaussian noise to the actions."""

    def __init__(
        self,
        environment: dm_env.Environment,
        scale: float = 0.01,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__(environment)

        action_spec = self._environment.action_spec()
        if not (
            np.all(np.isfinite(action_spec.minimum))
            and np.all(np.isfinite(action_spec.maximum))
        ):
            raise ValueError(_BOUNDS_MUST_BE_FINITE.format(action_spec=action_spec))
        self._minimum = action_spec.minimum
        self._maximum = action_spec.maximum
        self._noise_std = scale * (self._maximum - self._minimum)

        if hasattr(self._environment, "random_state"):
            self._rng = self._environment.random_state
        elif hasattr(self._environment, "task"):
            self._rng = self._environment.task.random
        else:
            self._rng = np.random.RandomState(seed=seed)

    def step(self, action) -> dm_env.TimeStep:
        noisy_action = action + self._rng.normal(scale=self._noise_std)
        np.clip(noisy_action, self._minimum, self._maximum, out=noisy_action)
        return self._environment.step(noisy_action)
