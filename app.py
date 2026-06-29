from __future__ import annotations

import argparse
import time
from datetime import datetime
from pathlib import Path

from faster_whisper import WhisperModel

from config.whisper_config import load_config
from core.summarizer import generate_summary
from utils.logger import get_logger
from utils.media_converter import convert_audio_to_wav, format_timestamp

logger = None


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="VoiceScribe: offline audio transcription and summary generation."
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to YAML configuration file. Defaults to config/audio_config.yaml.",
    )
    parser.add_argument(
        "--audio",
        help="Override the selected audio file path or filename.",
    )
    parser.add_argument(
        "--model",
        help="Whisper model name to use for transcription.",
    )
    parser.add_argument(
        "--language",
        help="Language code for transcription.",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        help="Beam size for transcription decoding.",
    )
    parser.add_argument(
        "--vad",
        dest="vad_filter",
        action="store_true",
        help="Enable voice activity detection.",
    )
    parser.add_argument(
        "--no-vad",
        dest="vad_filter",
        action="store_false",
        help="Disable voice activity detection.",
    )
    parser.set_defaults(vad_filter=None)
    parser.add_argument(
        "--skip-conversion",
        action="store_true",
        help="Skip audio conversion and assume the input file is already WAV.",
    )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="Skip the summary generation stage.",
    )
    parser.add_argument(
        "--transcripts-folder",
        help="Override transcript output folder.",
    )
    parser.add_argument(
        "--summaries-folder",
        help="Override summary output folder.",
    )
    parser.add_argument(
        "--logs-folder",
        help="Override logs folder.",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity.",
    )
    parser.add_argument(
        "--ffmpeg-path",
        help="Path to ffmpeg executable.",
    )
    parser.add_argument(
        "--summary-model",
        help="Model name for Ollama summary generation.",
    )
    parser.add_argument(
        "--prompt-template",
        help="Custom prompt template for summary generation. Use {transcript} to include transcript content.",
    )
    return parser


def apply_cli_overrides(config: dict, args: argparse.Namespace) -> dict:
    if args.audio:
        audio_path = Path(args.audio)
        if not audio_path.is_absolute() and not audio_path.exists():
            candidate = Path("audio") / audio_path
            if candidate.exists():
                audio_path = candidate
        config["audio_file"] = str(audio_path)

    if args.model:
        config["whisper"]["model"] = args.model
    if args.language:
        config["whisper"]["language"] = args.language
    if args.beam_size is not None:
        config["whisper"]["beam_size"] = args.beam_size
    if args.vad_filter is not None:
        config["whisper"]["vad_filter"] = args.vad_filter
    if args.skip_conversion:
        config["pipeline"]["skip_conversion"] = True
    if args.skip_summary:
        config["pipeline"]["skip_summary"] = True
    if args.transcripts_folder:
        config["output"]["transcripts_folder"] = args.transcripts_folder
    if args.summaries_folder:
        config["output"]["summaries_folder"] = args.summaries_folder
    if args.logs_folder:
        config["output"]["logs_folder"] = args.logs_folder
    if args.log_level:
        config["logging"]["level"] = args.log_level
    if args.ffmpeg_path:
        config["ffmpeg"]["path"] = args.ffmpeg_path
    if args.summary_model:
        config["summary"]["model"] = args.summary_model
    if args.prompt_template:
        config["summary"]["prompt_template"] = args.prompt_template

    return config


def generate_output_file_path(audio_file: str, transcripts_folder: str) -> Path:
    input_file_path = Path(audio_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"{input_file_path.stem}_{timestamp}.txt"

    transcripts_directory = Path(transcripts_folder)
    transcripts_directory.mkdir(parents=True, exist_ok=True)

    return transcripts_directory / output_file_name


def load_whisper_model(config: dict) -> WhisperModel:
    whisper_settings = config["whisper"]
    model_name = whisper_settings["model"]
    try:
        logger.info(f"Loading Faster Whisper model: {model_name}")
        return WhisperModel(
            model_name,
            device=whisper_settings["device"],
            compute_type=whisper_settings["compute_type"],
        )
    except Exception as error:
        logger.exception(f"Failed to load Faster Whisper model: {model_name}")
        raise


def validate_audio_file(audio_file: str) -> None:
    audio_path = Path(audio_file)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    logger.info(f"Validated audio file: {audio_file}")


def transcribe_audio(model, audio_file: str, config: dict) -> str:
    logger.info(f"Started transcription for file: {audio_file}")
    validate_audio_file(audio_file)
    whisper_settings = config["whisper"]
    try:
        segments, _info = model.transcribe(
            audio_file,
            beam_size=whisper_settings["beam_size"],
            language=whisper_settings["language"],
            vad_filter=whisper_settings["vad_filter"],
        )
    except Exception as error:
        logger.exception(f"Transcription failed for file: {audio_file}")
        raise

    formatted_transcript = []
    for segment in segments:
        start_time = format_timestamp(segment.start)
        end_time = format_timestamp(segment.end)
        text = segment.text.strip()
        formatted_transcript.append(f"[{start_time}s - {end_time}s] {text}")

    logger.info(f"Completed transcription for file: {audio_file}")
    return "\n".join(formatted_transcript)


def save_transcript(transcript_text: str, output_file_path: Path) -> None:
    sig_encoding = "utf-8-sig"
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_path, "w", encoding=sig_encoding) as file:
        file.write(transcript_text)
    logger.info(f"Transcript saved to: {output_file_path}")


def save_summary(summary_text: str, output_file_path: Path, summaries_folder: str) -> None:
    summary_directory = Path(summaries_folder)
    summary_directory.mkdir(parents=True, exist_ok=True)
    summary_file = summary_directory / f"{output_file_path.stem}_summary.txt"
    with open(summary_file, "w", encoding="utf-8-sig") as file:
        file.write(summary_text)
    logger.info(f"Summary saved to: {summary_file}")


def run_audio_conversion(config: dict) -> tuple[str, Path]:
    audio_file = config["audio_file"]
    ffmpeg_path = config["ffmpeg"]["path"]
    skip_conversion = config["pipeline"]["skip_conversion"]

    if skip_conversion or Path(audio_file).suffix.lower() == ".wav":
        logger.info("Skipping audio conversion stage.")
        processed_audio_file = audio_file
    else:
        logger.info("Started audio conversion stage.")
        processed_audio_file = convert_audio_to_wav(audio_file, ffmpeg_path)

    output_file_path = generate_output_file_path(
        processed_audio_file,
        config["output"]["transcripts_folder"],
    )
    logger.info("Audio conversion stage completed.")
    return processed_audio_file, output_file_path


def run_transcription(processed_audio_file: str, output_file_path: Path, config: dict) -> Path:
    logger.info("Started transcription stage.")
    whisper_model = load_whisper_model(config)
    transcript_text = transcribe_audio(whisper_model, processed_audio_file, config)
    save_transcript(transcript_text, output_file_path)
    logger.info("Completed transcription stage.")
    return output_file_path


def run_summary_generation(transcript_file_path: Path, config: dict) -> None:
    if config["pipeline"]["skip_summary"]:
        logger.info("Skipping summary generation stage.")
        return

    logger.info("Started summary generation stage.")
    with open(transcript_file_path, "r", encoding="utf-8-sig") as file:
        transcript_text = file.read()

    summary_text = generate_summary(
        transcript_text,
        model_name=config["summary"]["model"],
        prompt_template=config["summary"]["prompt_template"],
    )
    save_summary(summary_text, transcript_file_path, config["output"]["summaries_folder"])
    logger.info("Completed summary generation stage.")


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    config = load_config(args.config, start_folder=".")
    config = apply_cli_overrides(config, args)

    global logger
    logger = get_logger(
        logger_name="voicescribe",
        log_folder=config["output"]["logs_folder"],
        log_level=config["logging"]["level"],
    )

    try:
        logger.info("VoiceScribe execution started.")
        processed_audio_file, output_file_path = run_audio_conversion(config)
        transcript_file_path = run_transcription(processed_audio_file, output_file_path, config)
        run_summary_generation(transcript_file_path, config)
        logger.info("VoiceScribe execution completed successfully.")
        return 0
    except Exception as error:
        logger.exception(f"VoiceScribe execution failed. Error: {error}")
        return 1


if __name__ == "__main__":
    start_time = time.time()
    exit_code = main()
    execution_time = round(time.time() - start_time, 2)
    if logger is not None:
        logger.info(f"Execution completed in {execution_time} seconds")
    exit(exit_code)
