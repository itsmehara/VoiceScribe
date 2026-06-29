from collections import namedtuple
from pathlib import Path
from typing import Any

import yaml

WhisperModels = namedtuple(
    "WhisperModels",
    ["TINY", "BASE", "SMALL", "MEDIUM", "LARGE"],
)

WHISPER_MODELS = WhisperModels(
    TINY="tiny",
    BASE="base",
    SMALL="small",
    MEDIUM="medium",
    LARGE="large",
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_FILE = Path(__file__).resolve().parent / "audio_config.yaml"
LOCAL_CONFIG_NAMES = ["config.yaml", "audio_config.yaml"]

DEFAULT_CONFIG = {
    "selected_audio": None,
    "whisper": {
        "model": WHISPER_MODELS.MEDIUM,
        "device": "cpu",
        "compute_type": "int8",
        "language": "en",
        "vad_filter": True,
        "beam_size": 5,
    },
    "summary": {
        "model": "qwen3:4b",
        "prompt_template": None,
    },
    "output": {
        "transcripts_folder": "transcripts",
        "summaries_folder": "summaries",
        "logs_folder": "logs",
    },
    "pipeline": {
        "skip_conversion": False,
        "skip_summary": False,
    },
    "ffmpeg": {
        "path": "ffmpeg",
    },
    "logging": {
        "level": "INFO",
    },
}

LanguageCodes = namedtuple(
    "LanguageCodes",
    [
        "TELUGU",
        "HINDI",
        "TAMIL",
        "KANNADA",
        "MALAYALAM",
        "BENGALI",
        "MARATHI",
        "GUJARATI",
        "PUNJABI",
        "URDU",
        "ODIA",
        "ASSAMESE",
        "SANSKRIT",
        "ENGLISH",
        "SPANISH",
        "FRENCH",
        "GERMAN",
        "ITALIAN",
        "PORTUGUESE",
        "RUSSIAN",
        "CHINESE",
        "JAPANESE",
        "KOREAN",
        "ARABIC",
        "TURKISH",
        "DUTCH",
        "POLISH",
    ],
)

LANGUAGE_CODES = LanguageCodes(
    TELUGU="te",
    HINDI="hi",
    TAMIL="ta",
    KANNADA="kn",
    MALAYALAM="ml",
    BENGALI="bn",
    MARATHI="mr",
    GUJARATI="gu",
    PUNJABI="pa",
    URDU="ur",
    ODIA="or",
    ASSAMESE="as",
    SANSKRIT="sa",
    ENGLISH="en",
    SPANISH="es",
    FRENCH="fr",
    GERMAN="de",
    ITALIAN="it",
    PORTUGUESE="pt",
    RUSSIAN="ru",
    CHINESE="zh",
    JAPANESE="ja",
    KOREAN="ko",
    ARABIC="ar",
    TURKISH="tr",
    DUTCH="nl",
    POLISH="pl",
)


def _merge_config(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged


def resolve_audio_path(selected_audio: str, base_path: Path | None = None) -> Path:
    candidate = Path(selected_audio)
    if candidate.is_absolute():
        return candidate

    if base_path is None:
        base_path = REPO_ROOT

    if candidate.parent != Path('.'):
        return base_path / candidate

    return base_path / "audio" / candidate


def find_local_config(start_path: Path | str) -> Path | None:
    start_path = Path(start_path).resolve()
    if start_path.is_file():
        start_path = start_path.parent

    for config_name in LOCAL_CONFIG_NAMES:
        candidate = start_path / config_name
        if candidate.exists():
            return candidate

    return None


def load_config(config_file: str | Path | None = None, start_folder: str | Path | None = None) -> dict[str, Any]:
    if config_file:
        config_path = Path(config_file)
    else:
        config_path = None
        if start_folder:
            config_path = find_local_config(start_folder)
        if config_path is None:
            config_path = DEFAULT_CONFIG_FILE

    config_path = Path(config_path)
    if not config_path.exists():
        raise RuntimeError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            user_config = yaml.safe_load(file) or {}
    except Exception as error:
        raise RuntimeError(f"Failed to load configuration: {error}")

    config = _merge_config(DEFAULT_CONFIG, user_config)
    if not config.get("selected_audio"):
        raise RuntimeError("Missing 'selected_audio' in configuration")

    if config_path == DEFAULT_CONFIG_FILE:
        audio_base = REPO_ROOT
    else:
        audio_base = config_path.parent

    config["audio_file"] = str(resolve_audio_path(config["selected_audio"], base_path=audio_base))
    config["config_path"] = str(config_path)
    return config
