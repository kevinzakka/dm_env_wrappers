"""Tests for dm_env_wrappers."""

from absl.testing import absltest

import dm_env_wrappers


class DmEnvWrappersTest(absltest.TestCase):
    """Test that dm_env_wrappers can be imported correctly."""

    def test_import(self) -> None:
        self.assertTrue(hasattr(dm_env_wrappers, "EnvironmentWrapper"))


if __name__ == "__main__":
    absltest.main()
