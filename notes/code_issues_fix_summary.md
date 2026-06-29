# VoiceScribe Code Audit and Fixes

## Issues found

1. `config/whisper_config.py` loaded `config/audio_config.yaml` relative to the current working directory.
   - This could fail when installed as a package or when the current directory is not the repository root.
2. `utils/media_converter.py` did not validate that the source audio file exists before checking extension.
3. `pyproject.toml` did not include package data configuration, which means `config/audio_config.yaml` could be omitted from a wheel.

## Fixes applied

- Updated `config/whisper_config.py` to resolve the config file path relative to the package file.
- Added explicit missing file detection for audio input in `utils/media_converter.py`.
- Added local config discovery and override behavior in `config/whisper_config.py`.
- Added `include-package-data = true` and `config = ["*.yaml"]` to `pyproject.toml`.

## Notes

- The code imports now compile successfully inside the repository virtual environment.
- Future package refactor should move `app.py` into a proper package module for cleaner CLI support.
- `ffmpeg` and local Ollama models still remain required runtime prerequisites.
