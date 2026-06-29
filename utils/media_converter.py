from pathlib import Path
import subprocess

from utils.logger import get_logger

logger = get_logger()


def format_timestamp(seconds: float) -> str:
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    remaining_seconds = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


def convert_audio_to_wav(input_audio_file: str, ffmpeg_path: str = "ffmpeg") -> str:
    input_file_path = Path(input_audio_file)
    if not input_file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {input_audio_file}")

    supported_extensions = {".aac", ".mp3", ".m4a", ".ogg", ".opus", ".flac", ".wav"}
    if input_file_path.suffix.lower() not in supported_extensions:
        raise ValueError(f"Unsupported audio format: {input_file_path.suffix}")

    if input_file_path.suffix.lower() == ".wav":
        logger.info(f"Audio already in WAV format: {input_audio_file}")
        return str(input_file_path)

    output_wav_file = input_file_path.with_suffix(".wav")
    try:
        logger.info(f"Started audio conversion: {input_audio_file}")
        command = [ffmpeg_path, "-y", "-i", str(input_file_path), str(output_wav_file)]
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Audio conversion completed: {output_wav_file}")
        return str(output_wav_file)
    except Exception as error:
        logger.exception(f"Failed audio conversion: {error}")
        raise
