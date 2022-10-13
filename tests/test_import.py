"""Test that the wrappers can be imported and used."""

from absl.testing import absltest, parameterized
from dm_control.suite import load

from dm_env_wrappers import __all__ as wrappers
from dm_env_wrappers import wrap_all

wrappers = [w for w in wrappers if w.endswith("Wrapper")]


class ImportTest(parameterized.TestCase):
    """Test that the wrappers can be imported and used."""

    @parameterized.parameters(wrappers)
    def test_import_and_wrap(self, wrapper_str) -> None:
        env = load("cartpole", "balance")
        wrapped_env = getattr(__import__("dm_env_wrappers"), wrapper_str)(env)
        wrapped_env.reset()

    def test_wrap_all(self) -> None:
        env = load("cartpole", "balance")
        wrapper_cls = [getattr(__import__("dm_env_wrappers"), w) for w in wrappers]
        wrapped_env = wrap_all(env, wrapper_cls)
        wrapped_env.reset()


if __name__ == "__main__":
    absltest.main()
