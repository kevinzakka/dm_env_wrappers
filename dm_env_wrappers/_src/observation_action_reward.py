"""A wrapper that puts the previous action and reward into the observation."""

import dm_env
import tree

from dm_env_wrappers._src import base


class ObservationActionRewardWrapper(base.EnvironmentWrapper):
    """Wrapper that puts the previous action and reward into the observation."""

    def __init__(self, environment: dm_env.Environment) -> None:
        super().__init__(environment)

        # Enforce that the wrapped environment has a dict observation spec, i.e., that
        # is hasn't been wrapped with `ConcatObservationWrapper`.
        if not isinstance(self._environment.observation_spec(), dict):
            raise ValueError(
                "ObservationActionRewardWrapper requires an environment with a "
                "dictionary observation. Consider using this wrapper before "
                "ConcatObservationWrapper."
            )

        self._obs_spec = self._environment.observation_spec()
        self._obs_spec["action"] = self._environment.action_spec()
        self._obs_spec["reward"] = self._environment.reward_spec()

    def reset(self) -> dm_env.TimeStep:
        action = tree.map_structure(
            lambda x: x.generate_value(), self._environment.action_spec()
        )
        reward = tree.map_structure(
            lambda x: x.generate_value(), self._environment.reward_spec()
        )
        timestep = self._environment.reset()
        return self._augment_observation(action, reward, timestep)

    def step(self, action) -> dm_env.TimeStep:
        timestep = self._environment.step(action)
        return self._augment_observation(action, timestep.reward, timestep)

    def observation_spec(self):
        return self._obs_spec

    # Helper methods.

    def _augment_observation(
        self, action, reward, timestep: dm_env.TimeStep
    ) -> dm_env.TimeStep:
        observation = timestep.observation
        observation["action"] = action
        observation["reward"] = reward
        return timestep._replace(observation=observation)
