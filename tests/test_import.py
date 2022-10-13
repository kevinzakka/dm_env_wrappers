"""Test that the wrappers can be imported and used."""

from absl.testing import absltest, parameterized
from dm_control.suite import load

# Get a list of all the wrappers in the package.
from dm_env_wrappers import __all__ as wrappers


class ImportTest(parameterized.TestCase):
    """Test that the wrappers can be imported and used."""

    @parameterized.parameters(wrappers)
    def test_import_and_wrap(self, wrapper_str) -> None:
        env = load("cartpole", "balance")
        wrapped_env = getattr(__import__("dm_env_wrappers"), wrapper_str)(env)
        wrapped_env.reset()


if __name__ == "__main__":
    absltest.main()
