# `dm_env_wrappers`

[![PyPI Python Version][pypi-versions-badge]][pypi]
[![PyPI version][pypi-badge]][pypi]
[![dexterity-tests][tests-badge]][tests]

[pypi-versions-badge]: https://img.shields.io/pypi/pyversions/dm_env_wrappers
[pypi-badge]: https://badge.fury.io/py/dm_env_wrappers.svg
[pypi]: https://pypi.org/project/dm_env_wrappers/
[tests-badge]: https://github.com/kevinzakka/dm_env_wrappers/actions/workflows/build.yml/badge.svg
[tests]: https://github.com/kevinzakka/dm_env_wrappers/actions/workflows/build.yml

`dm_env_wrappers` is a collection of frequently-used wrappers for environments that respect the [dm_env](https://github.com/deepmind/dm_env) interface (e.g., dm_control suite, composer, etc.). The wrappers have been extracted out of [acme](https://github.com/deepmind/acme) and are now available as a standalone library.

## Installation (Python 3.7+)

```bash
pip install --upgrade dm_env_wrappers
```

## Acknowledgements

All credit goes to DeepMind for the original implementation of these wrappers.
