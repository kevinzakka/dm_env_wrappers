"""Tests for action_noise.py."""

import numpy as np
from absl.testing import absltest
from dm_control.manipulation import load as load_manipulation
from dm_control.suite import load as load_suite
from dm_env import specs

from dm_env_wrappers import ActionNoiseWrapper


class ActionNoiseWrapperTest(absltest.TestCase):
    def test_on_suite_env(self):
        """Tests that the wrapper works on a suite environment."""
        env = load_suite("cartpole", "balance")
        env = ActionNoiseWrapper(env, scale=0.1)
        action_spec = env.action_spec()
        assert isinstance(action_spec, specs.BoundedArray)
        zero_action = np.zeros_like(action_spec.minimum)
        env.reset()
        env.step(zero_action)

    def test_on_manipulation_env(self):
        """Tests that the wrapper works on a manipulation environment."""
        env = load_manipulation(environment_name="stack_2_bricks_features", seed=12345)
        env = ActionNoiseWrapper(env, scale=0.1)
        action_spec = env.action_spec()
        assert isinstance(action_spec, specs.BoundedArray)
        zero_action = np.zeros_like(action_spec.minimum)
        env.reset()
        env.step(zero_action)


if __name__ == "__main__":
    absltest.main()
