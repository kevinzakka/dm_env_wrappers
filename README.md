# `dm_env_wrappers`

[![PyPI Python Version][pypi-versions-badge]][pypi]
[![PyPI version][pypi-badge]][pypi]
[![dexterity-tests][tests-badge]][tests]

[pypi-versions-badge]: https://img.shields.io/pypi/pyversions/dm_env_wrappers
[pypi-badge]: https://badge.fury.io/py/dm_env_wrappers.svg
[pypi]: https://pypi.org/project/dm_env_wrappers/
[tests-badge]: https://github.com/kevinzakka/dm_env_wrappers/actions/workflows/build.yml/badge.svg
[tests]: https://github.com/kevinzakka/dm_env_wrappers/actions/workflows/build.yml

`dm_env_wrappers` is a collection of frequently-used wrappers for environments that respect the [dm_env](https://github.com/deepmind/dm_env) interface (e.g., dm_control suite, composer, etc.).

*Note: `dm_env_wrappers` is not affiliated with DeepMind or the [`acme`](https://github.com/deepmind/acme) library. Some wrappers were simply extracted out of the `acme` codebase to be more easily installable and reused across various projects. While `dm_env_wrappers` contains some wrappers that are not in `acme`, all `acme` original wrappers are clearly marked as such and retain their original Apache 2.0 License.*

<details>
  <summary>Available Wrappers</summary>
  <br/>

| Wrapper                                | Description                                          |
|----------------------------------------|------------------------------------------------------|
| `ActionNoiseWrapper`                   | Adds Gaussian noise to the actions.                  |
| `ActionRepeatWrapper`                  | Repeats the same action for a given number of steps. |
| `CanonicalSpecWrapper`                 | Converts action specs to canonical form.             |
| `ConcatObservationWrapper`             | Concatenate observation fields into array.           |
| `EpisodeStatisticsWrapper`             | Track episode length and return.                     |
| `ExpandScalarObservationShapesWrapper` | Expands scalar shapes in the observation.            |
| `FrameStackingWrapper`                 | Stacks observations along a new final axis.          |
| `SinglePrecisionWrapper`               | Converts all spec dtypes to single precision.        |
| `StepLimitWrapper`                     | Limits the number of steps in an episode.            |

</details>

## Installation (Python 3.7+)

```bash
pip install --upgrade dm_env_wrappers
```

## Contributing

If you find a bug or would like to add a new wrapper, please feel free to open an [issue](https://github.com/kevinzakka/dm_env_wrappers/issues) or submit a [PR](https://github.com/kevinzakka/dm_env_wrappers/pulls)!
