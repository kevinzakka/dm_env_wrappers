"""Tests for step_limit.py."""

from absl.testing import absltest
from dm_control.suite import load as load_suite

from dm_env_wrappers._src import step_limit


class StepLimitWrapperTest(absltest.TestCase):
    """Tests for StepLimitWrapper."""

    def test_raises_value_error_on_negative_limit(self) -> None:
        env = load_suite("cartpole", "balance")
        with self.assertRaises(ValueError):
            step_limit.StepLimitWrapper(env, step_limit=-1)

    def test_raises_value_error_on_non_integer_limit(self) -> None:
        env = load_suite("cartpole", "balance")
        with self.assertRaises(ValueError):
            step_limit.StepLimitWrapper(env, step_limit=0.5)  # type: ignore


if __name__ == "__main__":
    absltest.main()
