"""A wrapper for recording and rendering dm_control environments."""

import math
from typing import Optional, Union

import dm_env
import numpy as np

from dm_env_wrappers._src import video


class DmControlVideoWrapper(video.VideoWrapper):
    """Records and renders episodes for `dm_control` environments."""

    def __init__(
        self,
        environment: dm_env.Environment,
        *,
        frame_rate: Optional[int] = None,
        camera_id: Optional[Union[str, int]] = None,
        height: int = 480,
        width: int = 640,
        playback_speed: float = 1.0,
        **kwargs,
    ) -> None:
        # Check that the environment is a dm_control environment.
        if not hasattr(environment, "physics"):
            raise ValueError("VideoWrapper only works with dm_control environments.")

        if frame_rate is None:
            try:
                control_timestep = getattr(environment, "control_timestep")()
                frame_rate = int(playback_speed / control_timestep)
            except AttributeError as e:
                raise AttributeError(
                    "Environment must have a control_timestep() method."
                ) from e

        super().__init__(environment, frame_rate=frame_rate, **kwargs)
        self._camera_id = camera_id
        self._height = height
        self._width = width

        # Ensure the offscreen framebuffer is large enough to accommodate the requested
        # resolution.
        new_offwidth = max(self.physics.model.vis.global_.offwidth, width)
        new_offheight = max(self.physics.model.vis.global_.offheight, height)
        mjcf_model = self._task.root_entity.mjcf_model
        mjcf_model.visual.__getattr__("global").offheight = new_offheight
        mjcf_model.visual.__getattr__("global").offwidth = new_offwidth

    # Helper methods.

    def _render_frame(self, observation) -> np.ndarray:
        del observation  # Unused.
        physics = self.environment.physics
        if self._camera_id is not None:
            return physics.render(
                camera_id=self._camera_id,
                height=self._height,
                width=self._width,
            )
        # If no camera_id is specified, render all cameras in a grid.
        num_cameras = physics.model.ncam
        num_columns = int(math.ceil(math.sqrt(num_cameras)))
        num_rows = int(math.ceil(float(num_cameras) / num_columns))
        height = self._height
        width = self._width
        frame = np.zeros((num_rows * height, num_columns * width, 3), dtype=np.uint8)
        for col in range(num_columns):
            for row in range(num_rows):
                camera_id = row * num_columns + col
                if camera_id >= num_cameras:
                    break
                subframe = physics.render(
                    camera_id=camera_id, height=height, width=width
                )
                frame[
                    row * height : (row + 1) * height, col * width : (col + 1) * width
                ] = subframe
        return frame
