"""Test for dm_env_wrappers."""

from absl.testing import absltest, parameterized
from dm_control.suite import load

from dm_env_wrappers import __all__, wrap_all

_WRAPPERS = [w for w in __all__ if w.endswith("Wrapper")]


class ImportTest(parameterized.TestCase):
    """Test that the wrappers can be imported and used."""

    @parameterized.parameters(_WRAPPERS)
    def test_import_and_wrap(self, wrapper_str) -> None:
        env = load("cartpole", "balance")
        wrapped_env = getattr(__import__("dm_env_wrappers"), wrapper_str)(env)
        wrapped_env.reset()

    def test_wrap_all(self) -> None:
        env = load("cartpole", "balance")
        wrapper_cls = [getattr(__import__("dm_env_wrappers"), w) for w in _WRAPPERS]
        wrapped_env = wrap_all(env, wrapper_cls)
        wrapped_env.reset()


if __name__ == "__main__":
    absltest.main()
