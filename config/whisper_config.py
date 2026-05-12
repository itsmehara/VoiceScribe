from collections import namedtuple


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
SELECTED_MODEL = WHISPER_MODELS.SMALL


# Input audio file
AUDIO_FILE = "audio/Project_notes_12 May_4_44_pm.aac"


# Output folders
TRANSCRIPTS_FOLDER = "transcripts"
LOG_FOLDER = "logs"