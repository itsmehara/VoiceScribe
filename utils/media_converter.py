from pathlib import Path
import subprocess
from utils.logger import get_logger
logger = get_logger()


def format_timestamp(seconds: float) -> str:
    """
    Converts seconds into HH:MM:SS format.
    """

    total_seconds = int(seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    remaining_seconds = total_seconds % 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{remaining_seconds:02d}"
    )

def convert_audio_to_wav(input_audio_file: str) -> str:
    """
    Converts AAC audio file into WAV format using FFmpeg.
    Returns converted WAV file path.
    """

    input_file_path = Path(input_audio_file)
    output_wav_file = input_file_path.parent / f"{input_file_path.stem}.wav"

    try:
        logger.info(f"Started AAC to WAV conversion: {input_audio_file}")

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_file_path),
            str(output_wav_file)
        ]

        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

        logger.info(f"WAV conversion completed: {output_wav_file}")

        return str(output_wav_file)

    except Exception as error:
        logger.exception(f"Failed AAC to WAV conversion: {error}")
        raise error
