"""Wrapper that tracks episode statistics."""

from collections import deque
from typing import Deque, Dict

import dm_env

from dm_env_wrappers._src import base


class EpisodeStatisticsWrapper(base.EnvironmentWrapper):
    """Wrapper for tracking an episode's statistics.

    This wrapper tracks the length and return of the last `deque_size` episodes. The
    mean length and return can be retrieved using `get_mean_length` and
    `get_mean_return` respectively.
    """

    def __init__(self, environment: dm_env.Environment, deque_size: int = 100) -> None:
        super().__init__(environment)

        self._episode_return: float = 0.0
        self._episode_length: int = 0
        self._return_queue: Deque[float] = deque(maxlen=deque_size)
        self._length_queue: Deque[int] = deque(maxlen=deque_size)

    def reset(self) -> dm_env.TimeStep:
        self._episode_return = 0.0
        self._episode_length = 0
        return self._environment.reset()

    def step(self, action) -> dm_env.TimeStep:
        timestep = self._environment.step(action)
        self._episode_return += timestep.reward
        self._episode_length += 1
        if timestep.last():
            self._return_queue.append(self._episode_return)
            self._length_queue.append(self._episode_length)
            self._episode_return = 0.0
            self._episode_length = 0
        return timestep

    def get_mean_return(self) -> float:
        """Returns the mean return of the last `deque_size` episodes."""
        if not self._return_queue:
            return 0.0
        return sum(self._return_queue) / len(self._return_queue)

    def get_mean_length(self) -> float:
        """Returns the mean length of the last `deque_size` episodes."""
        if not self._length_queue:
            return 0.0
        return sum(self._length_queue) / len(self._length_queue)

    def get_statistics(self) -> Dict[str, float]:
        """Returns the mean return / length of the last `deque_size` episodes."""
        return {
            "mean_return": self.get_mean_return(),
            "mean_length": self.get_mean_length(),
        }
