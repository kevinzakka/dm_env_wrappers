"""Tests for statistics.py."""

import dm_env
from absl.testing import absltest

from dm_env_wrappers._src import episode_statistics, step_limit


class _FakeEnvironment(dm_env.Environment):
    """A mock environment for testing."""

    def reset(self) -> dm_env.TimeStep:
        return dm_env.restart(0)

    def step(self, action) -> dm_env.TimeStep:
        del action  # Unused.
        return dm_env.transition(1, 1, 1)

    def observation_spec(self):
        return None

    def action_spec(self):
        return None


class EpisodeStatisticsWrapper(absltest.TestCase):
    """Tests for EpisodeStatisticsWrapper."""

    def test_returns_zero_at_init(self) -> None:
        environment = _FakeEnvironment()
        environment = episode_statistics.EpisodeStatisticsWrapper(environment)
        self.assertEqual(environment.get_mean_return(), 0.0)
        self.assertEqual(environment.get_mean_length(), 0.0)

    def test_episode_statistics(self):
        """Tests that the wrapper returns the correct statistics."""
        environment = _FakeEnvironment()
        environment = step_limit.StepLimitWrapper(environment, 5)
        environment = episode_statistics.EpisodeStatisticsWrapper(environment)

        # Run 100 episodes.
        for _ in range(100):
            timestep = environment.reset()
            while not timestep.last():
                timestep = environment.step(0)

        self.assertEqual(environment.get_mean_return(), 5.0)
        self.assertEqual(environment.get_mean_length(), 5.0)


if __name__ == "__main__":
    absltest.main()
