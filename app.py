from datetime import datetime
from pathlib import Path
import time
from faster_whisper import WhisperModel

from config.whisper_config import AUDIO_FILE, SELECTED_MODEL, TRANSCRIPTS_FOLDER
from utils.logger import get_logger
from utils.media_converter import convert_audio_to_wav, format_timestamp
from core.summarizer import generate_summary
from config.whisper_config import SUMMARIES_FOLDER

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
    Loads Faster Whisper model.
    """
    try:
        logger.info(f"Loading Faster Whisper model: {model_name}")
        return WhisperModel(
            model_name,
            device="cpu",
            compute_type="int8"
        )
    except Exception as error:
        logger.exception(f"Failed to load Faster Whisper model: {model_name}")
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
        segments, info = model.transcribe(audio_file, beam_size=5, language="en", vad_filter=True)
    except Exception as error:
        logger.exception(f"Transcription failed for file: {audio_file}")
        raise error

    formatted_transcript = []

    for segment in segments:
        start_time = format_timestamp(segment.start)
        end_time = format_timestamp(segment.end)
        text = segment.text.strip()
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
    with open(output_file_path, "w", encoding=sig_encoding) as file:
        file.write(transcript_text)

    logger.info(f"Transcript saved to: {output_file_path}")


def save_summary(summary_text: str, output_file_path: Path) -> None:
    summary_directory = Path(SUMMARIES_FOLDER)
    summary_directory.mkdir(exist_ok=True)
    summary_file = summary_directory / f"{output_file_path.stem}_summary.txt"
    with open(summary_file, "w", encoding="utf-8-sig") as file: file.write(summary_text)
    logger.info(f"Summary saved to: {summary_file}")


def run_audio_conversion() -> tuple[str, Path]:
    logger.info("Started audio conversion stage.")
    processed_audio_file = convert_audio_to_wav(AUDIO_FILE)
    output_file_path = generate_output_file_path(processed_audio_file)
    logger.info("Completed audio conversion stage.")
    return processed_audio_file, output_file_path


def run_transcription(processed_audio_file: str, output_file_path: Path) -> Path:
    logger.info("Started transcription stage.")
    whisper_model = load_whisper_model(SELECTED_MODEL)
    transcript_text = transcribe_audio(whisper_model, processed_audio_file)
    save_transcript(transcript_text, output_file_path)
    logger.info("Completed transcription stage.")
    return output_file_path


def run_summary_generation(transcript_file_path: Path) -> None:
    logger.info("Started summary generation stage.")
    with open(transcript_file_path, "r", encoding="utf-8-sig") as file:
        transcript_text = file.read()
    summary_text = generate_summary(transcript_text)
    save_summary(summary_text, transcript_file_path)
    logger.info("Completed summary generation stage.")


def main() -> None:
    try:
        logger.info("VoiceScribe execution started.")
        processed_audio_file, output_file_path = run_audio_conversion()
        transcript_file_path = run_transcription(processed_audio_file, output_file_path)
        run_summary_generation(transcript_file_path)
        logger.info("VoiceScribe execution completed successfully.")

    except Exception as error:
        logger.exception(f"VoiceScribe execution failed. Error: {error}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = round(time.time() - start_time, 2)
    logger.info(f"Execution completed in {execution_time} seconds")