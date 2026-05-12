from datetime import datetime
from pathlib import Path
import time
import whisper

from config.whisper_config import (
    AUDIO_FILE,
    SELECTED_MODEL,
    TRANSCRIPTS_FOLDER
)

from utils.logger import get_logger


logger = get_logger()


def generate_output_file_path(audio_file: str) -> Path:
    """
    Generates timestamp-based transcript output file path.
    """

    input_file_path = Path(audio_file)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file_name = (
        f"{input_file_path.stem}_{timestamp}.txt"
    )

    transcripts_directory = Path(TRANSCRIPTS_FOLDER)
    transcripts_directory.mkdir(exist_ok=True)

    return transcripts_directory / output_file_name


def load_whisper_model(model_name: str):
    """
    Loads Whisper model.
    """
    try:
        logger.info(
            f"Loading Whisper model: {model_name}"
        )
        return whisper.load_model(model_name)
    except Exception as error:
        logger.exception(
            f"Failed to load Whisper model: {model_name}"
        )
        raise


def validate_audio_file(audio_file: str) -> None:
    audio_path = Path(audio_file)
    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_file}"
        )

    logger.info(
        f"Validated audio file: {audio_file}"
    )


def transcribe_audio(model, audio_file: str) -> str:
    """
    Transcribes input audio file into text.
    """

    logger.info(
        f"Started transcription for file: {audio_file}"
    )

    validate_audio_file(audio_file)
    result = model.transcribe(audio_file)

    logger.info(
        f"Completed transcription for file: {audio_file}"
    )

    return result["text"]


def save_transcript(
        transcript_text: str,
        output_file_path: Path
) -> None:
    """
    Saves transcript into output text file.
    """

    with open(
            output_file_path,
            "w",
            encoding="utf-8"
    ) as file:
        file.write(transcript_text)

    logger.info(
        f"Transcript saved to: {output_file_path}"
    )


def main() -> None:
    """
    Main execution flow.
    """

    try:
        logger.info("VoiceScribe execution started.")

        output_file_path = generate_output_file_path(
            AUDIO_FILE
        )

        whisper_model = load_whisper_model(
            SELECTED_MODEL
        )

        transcript_text = transcribe_audio(
            whisper_model,
            AUDIO_FILE
        )

        save_transcript(
            transcript_text,
            output_file_path
        )

        logger.info(
            "VoiceScribe execution completed successfully."
        )

    except Exception as error:
        logger.exception(
            f"VoiceScribe execution failed. Error: {error}"
        )


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = round(time.time() - start_time, 2)
    logger.info(
        f"Execution completed in {execution_time} seconds"
    )