"""Tests for action_noise.py."""

import numpy as np
import tree
from absl.testing import absltest, parameterized
from dm_control.suite import load as load_suite

from dm_env_wrappers._src import action_noise

_SEED = 12345


class ActionNoiseWrapperTest(parameterized.TestCase):
    """Tests for ActionNoiseWrapper."""

    def test_raises_value_error_on_negative_scale(self) -> None:
        env = load_suite("cartpole", "balance")
        with self.assertRaises(ValueError):
            action_noise.ActionNoiseWrapper(env, scale=-0.1)

    @parameterized.product(
        (
            {"domain_name": "cartpole", "task_name": "balance"},
            {"domain_name": "humanoid", "task_name": "walk"},
        ),
        scale=(0.0, 0.1, 1.0),
    )
    def test_step_suite(self, domain_name: str, task_name: str, scale: float) -> None:
        def _get_env(domain_name: str, task_name: str):
            return load_suite(
                domain_name=domain_name,
                task_name=task_name,
                task_kwargs={"random": np.random.RandomState(_SEED)},
            )

        env = _get_env(domain_name, task_name)
        action_spec = env.action_spec()
        lower, upper = action_spec.minimum, action_spec.maximum
        wrapped_env = action_noise.ActionNoiseWrapper(env, scale=scale)

        std = scale * (upper - lower)
        expected_noise = np.random.RandomState(_SEED).normal(scale=std)
        action = np.random.RandomState(_SEED).uniform(lower, upper)
        expected_noisy_action = np.clip(action + expected_noise, lower, upper)

        wrapped_env.reset()
        # Reseed the random state in case it was called at episode initialization.
        wrapped_env._random_state.seed(_SEED)
        timestep = wrapped_env.step(action)
        actual_observation = timestep.observation

        env = _get_env(domain_name, task_name)
        env.reset()
        expected_timestep = env.step(expected_noisy_action)
        expected_observation = expected_timestep.observation

        tree.map_structure(
            np.testing.assert_array_equal, actual_observation, expected_observation
        )


if __name__ == "__main__":
    absltest.main()
