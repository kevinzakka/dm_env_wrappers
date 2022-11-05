"""Wrappers for validating specs."""

import dm_env

from dm_env_wrappers._src import base


class ValidateActionSpecWrapper(base.EnvironmentWrapper):
    """A wrapper that throws a `ValueError` if an action does not match its spec."""

    def step(self, action) -> dm_env.TimeStep:
        self.action_spec().validate(action)
        return self._environment.step(action)
