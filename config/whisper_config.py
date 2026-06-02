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
SELECTED_MODEL = WHISPER_MODELS.MEDIUM

upasana_hnb_discussion1 = "Project_notes_12 May_4_44_pm.aac"
upasana_hnb_discussion2 = "disc2_upasana_19May_4.49pm.aac"
aiml_kotni_discussion1 = "KotniRamu_Hara_18 May_8.37_am.aac"
upasana_kt_hnb_session1 = "upasana_kt_hnb_session_1 Jun_3.33 pm.aac"
upasana_kt_hnb_session01 = "upa_hnb_kt_1 Jun_ 3.33 pm.aac"
# Input audio file
AUDIO_FILE = f"audio/{upasana_kt_hnb_session01}"

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