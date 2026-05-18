from datetime import datetime
from pathlib import Path
import time
from faster_whisper import WhisperModel

from config.whisper_config import AUDIO_FILE, SELECTED_MODEL, TRANSCRIPTS_FOLDER, LANGUAGE_CODES
from utils.logger import get_logger
from utils.audio_converter import convert_aac_to_wav, format_timestamp

logger = get_logger()


def generate_output_file_path(audio_file: str) -> Path:
    """
    Generates timestamp-based transcript output file path.
    """
    input_file_path = Path(audio_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"{input_file_path.stem}_{timestamp}.txt"

    transcripts_directory = Path(TRANSCRIPTS_FOLDER)
    transcripts_directory.mkdir(exist_ok=True)

    return transcripts_directory / output_file_name


def load_whisper_model(model_name: str):
    """
    Loads Whisper model. # open-api whisper.
    """
    try:
        logger.info(f"Loading Whisper model: {model_name}")
        return whisper.load_model(model_name)
    except Exception as error:
        logger.exception(f"Failed to load Whisper model: {model_name}")
        raise error


def validate_audio_file(audio_file: str) -> None:
    """Validate audio file existence."""
    audio_path = Path(audio_file)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    logger.info(f"Validated audio file: {audio_file}")


def transcribe_audio(model, audio_file: str) -> str:
    """
    Transcribes input audio file into timestamp-based conversation text.
    """
    logger.info(f"Started transcription for file: {audio_file}")
    validate_audio_file(audio_file)
    try:
        result = model.transcribe(audio_file)
    except Exception as error:
        logger.exception(f"Transcription failed for file: {audio_file}")
        raise error

    formatted_transcript = []

    for segment in result["segments"]:
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        text = segment["text"].strip()
        formatted_transcript.append(
            f"[{start_time}s - {end_time}s] {text}"
        )
    logger.info(f"Completed transcription for file: {audio_file}")

    return "\n".join(formatted_transcript)


def save_transcript(transcript_text: str, output_file_path: Path) -> None:
    """
    Saves transcript into output text file.
    """
    sig_encoding = "utf-8-sig"
    utf_encoding = "utf-8"
    with open(output_file_path, "w", encoding=sig_encoding) as file:
        file.write(transcript_text)

    logger.info(f"Transcript saved to: {output_file_path}")


def main() -> None:
    """
    Main execution flow.
    """
    try:
        logger.info("VoiceScribe execution started.")
        processed_audio_file = convert_aac_to_wav(AUDIO_FILE)
        output_file_path = generate_output_file_path(processed_audio_file)
        whisper_model = load_whisper_model(SELECTED_MODEL)
        transcript_text = transcribe_audio(whisper_model, processed_audio_file)
        save_transcript(transcript_text, output_file_path)
        logger.info("VoiceScribe execution completed successfully.")
    except Exception as error:
        logger.exception(f"VoiceScribe execution failed. Error: {error}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = round(time.time() - start_time, 2)
    logger.info(f"Execution completed in {execution_time} seconds")