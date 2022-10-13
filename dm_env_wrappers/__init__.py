"""dm_env_wrappers: A collection of wrappers for dm_env environments."""

from dm_env_wrappers._src.action_noise import ActionNoiseWrapper
from dm_env_wrappers._src.action_repeat import ActionRepeatWrapper
from dm_env_wrappers._src.base import EnvironmentWrapper, wrap_all
from dm_env_wrappers._src.canonical_spec import CanonicalSpecWrapper
from dm_env_wrappers._src.concatenate_observations import ConcatObservationWrapper
from dm_env_wrappers._src.expand_scalar_observation_shapes import (
    ExpandScalarObservationShapesWrapper,
)
from dm_env_wrappers._src.frame_stacking import FrameStackingWrapper
from dm_env_wrappers._src.single_precision import SinglePrecisionWrapper
from dm_env_wrappers._src.step_limit import StepLimitWrapper

__version__ = "0.0.4"

__all__ = (
    "ActionNoiseWrapper",
    "ActionRepeatWrapper",
    "CanonicalSpecWrapper",
    "ConcatObservationWrapper",
    "EnvironmentWrapper",
    "ExpandScalarObservationShapesWrapper",
    "FrameStackingWrapper",
    "SinglePrecisionWrapper",
    "StepLimitWrapper",
    "wrap_all",
)

#  _________________________________________
# / Please don't use symbols in `_src` they \
# \ are not part of the public API.         /
#  -----------------------------------------
#         \   ^__^
#          \  (oo)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||
#
