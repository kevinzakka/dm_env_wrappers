"""A wrapper for logging to Weights & Biases."""

from typing import Any, Optional

import dm_env

from dm_env_wrappers._src import base


class WandbLoggerWrapper(base.EnvironmentWrapper):
    """Logs any environment methods decorated with @wblog to Weights & Biases.

    This wrapper will find all functions decorated with @wblog and log their return
    values to Weights & Biases when `.log()` is called. Any function decorated with
    @wblog must return a dictionary of key-value pairs, where they keys are strings
    and the values are scalars or numpy arrays.
    """

    def __init__(
        self,
        environment: dm_env.Environment,
        wandb_run: Any,
        prefix: Optional[str] = None,
    ) -> None:
        """Initializes the wrapper.

        Args:
            environment: The environment to wrap.
            wandb_run: The Weights & Biases run object.
            prefix: A prefix to add to all logged keys. The final key will be of the
                form "{prefix}/{key}".
        """
        super().__init__(environment)

        self._wandb_run = wandb_run
        self._prefix = prefix

        # Find all functions decorated with @wblog.
        self._wblogged_functions = []
        for name in dir(self._environment):
            attr = getattr(self._environment, name)
            if hasattr(attr, "_wblog"):
                self._wblogged_functions.append(attr)

        print("Logging the following functions to Weights & Biases:")
        for function in self._wblogged_functions:
            print(function.__name__)

    def log(self, step: int) -> None:
        """Logs all @wblogged functions to Weights & Biases.

        Args:
            step: The current step.
        """
        for function in self._wblogged_functions:
            values = function()
            if not isinstance(values, dict):
                raise ValueError(
                    f"Function {function.__name__} must return a dictionary."
                )
            if self._prefix is not None:
                values = {f"{self._prefix}/{k}": v for k, v in values.items()}
            self._wandb_run.log(values, step=step)


def wblog(function):
    """Decorator for logging a function's return value to Weights & Biases.

    The function must return a dictionary of key-value pairs, where they keys are
    strings and the values are scalars or numpy arrays.

    Args:
        function: The function to decorate.

    Returns:
        The decorated function.
    """
    function._wblog = True
    return function
