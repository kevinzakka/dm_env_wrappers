"""A wrapper to unify dm_control suite and composer environments."""

import numpy as np

from dm_env_wrappers._src import base


class DmControlWrapper(base.EnvironmentWrapper):
    """Gives a unified interface to `dm_control` environments."""

    @property
    def random_state(self) -> np.random.RandomState:
        if hasattr(self.environment, "random_state"):
            return self.environment.random_state
        return self.environment.task.random
