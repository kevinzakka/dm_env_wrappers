"""Base environment wrapper for rendering episodes as videos."""

import abc
from pathlib import Path
from typing import List

import dm_env
import imageio
import numpy as np

from dm_env_wrappers._src import base


class VideoWrapper(base.EnvironmentWrapper, abc.ABC):
    """Base wrapper for rendering episodes as videos.

    Subclasses must implement the `_render_frame` method.
    """

    def __init__(
        self,
        environment: dm_env.Environment,
        save_dir: str = "~/dm_env_wrappers",
        save_every: int = 100,
        frame_rate: int = 30,
    ) -> None:
        super().__init__(environment)

        self._save_dir = Path(save_dir).expanduser()
        self._save_dir.mkdir(parents=True, exist_ok=True)
        self._save_every = save_every
        self._frame_rate = frame_rate

        self._frames: List[np.ndarray] = []
        self._counter: int = 0

    def step(self, action) -> dm_env.TimeStep:
        timestep = self.environment.step(action)
        self._append_frame(timestep.observation)
        return timestep

    def reset(self) -> dm_env.TimeStep:
        if self._frames:
            self._write_frames()
        self._counter += 1
        timestep = self.environment.reset()
        self._append_frame(timestep.observation)
        return timestep

    # Helper methods.

    def _append_frame(self, observation):
        if self._counter % self._save_every == 0:
            self._frames.append(self._render_frame(observation))

    def _write_frames(self) -> None:
        if self._counter % self._save_every == 0:
            filename = self._save_dir / f"{self._counter:05d}.mp4"
            imageio.mimsave(
                str(filename), self._frames, fps=self._frame_rate  # type: ignore
            )

        # Clear frame buffer whether or not we wrote a video.
        self._frames = []

    @abc.abstractmethod
    def _render_frame(self, observation) -> np.ndarray:
        ...
