"""Wrappers for validating specs."""

import dm_env

from dm_env_wrappers._src import base


class ValidateActionSpecWrapper(base.EnvironmentWrapper):
    """Throws an exception if an action does not match its spec."""

    def step(self, action) -> dm_env.TimeStep:
        """Validates the action against the action spec.

        Raises:
            ValueError: If the action does not match the action spec.
        """
        self.action_spec().validate(action)
        return self._environment.step(action)
