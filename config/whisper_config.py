from collections import namedtuple
import yaml
from pathlib import Path

WhisperModels = namedtuple(
    "WhisperModels",
    ["TINY", "BASE", "SMALL", "MEDIUM", "LARGE"]
)

WHISPER_MODELS = WhisperModels(
    TINY="tiny",
    BASE="base",
    SMALL="small",
    MEDIUM="medium",
    LARGE="large"
)

# Default model selection
SELECTED_MODEL = WHISPER_MODELS.MEDIUM

config_file = Path("config/audio_config.yaml")
try:
    with open(config_file, "r") as file:
        audio_config = yaml.safe_load(file)
except Exception as error:
    raise RuntimeError(f"Failed to load configuration: {error}")

# Input audio file
AUDIO_FILE = f"audio/{audio_config['selected_audio']}"

# Output folders
TRANSCRIPTS_FOLDER = "transcripts"
LOG_FOLDER = "logs"

LanguageCodes = namedtuple(
    "LanguageCodes",
    [
        # Indian Languages
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

        # International Languages
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
    ]
)


LANGUAGE_CODES = LanguageCodes(
    # Indian Languages
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

    # International Languages
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