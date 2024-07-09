"""Tests for dm_env_wrappers."""

from absl.testing import absltest

import numpy as np
import dm_env_wrappers
import dm_env


class DmEnvWrappersTest(absltest.TestCase):
    """Test that dm_env_wrappers can be imported correctly."""

    def test_import(self) -> None:
        self.assertTrue(hasattr(dm_env_wrappers, "EnvironmentWrapper"))

    def test_canonical_spec_discrete_action(self) -> None:
        """Test that canonical spec wrapper works with discrete actions."""
        num_actions = 3
        action_dtype = np.int32
        class _FakeEnv(dm_env.Environment):
            def observation_spec(self):
                return dm_env.specs.Array(shape=(1,), dtype=float)

            def action_spec(self):
                return dm_env.specs.DiscreteArray(num_actions, dtype=action_dtype)

            def reset(self):
                return None

            def step(self, action):
                assert np.issubdtype(action.dtype, action_dtype)
                return dm_env.TimeStep(dm_env.StepType.FIRST, 0.0, 0.0, False)

        wrapped = dm_env_wrappers.CanonicalSpecWrapper(_FakeEnv())
        wrapped_spec = wrapped.action_spec()
        self.assertEqual(wrapped_spec.minimum, 0)
        self.assertEqual(wrapped_spec.maximum, num_actions - 1)
        wrapped.step(np.array(num_actions - 1, dtype=action_dtype))

if __name__ == "__main__":
    absltest.main()
