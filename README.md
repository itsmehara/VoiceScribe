# VoiceScribe

VoiceScribe is a privacy-first, offline speech-to-text application built with Python, Faster Whisper, and FFmpeg.

It converts meeting recordings, interviews, voice notes, and conversations into timestamped transcripts while running entirely on the local machine.

The project is designed with a modular architecture to support future AI-powered meeting intelligence capabilities.

---

# Current Features

* Local offline transcription
* Faster Whisper integration
* AAC, MP3, WAV, M4A, OGG, OPUS, and FLAC support
* Automatic audio-to-WAV conversion using FFmpeg
* Timestamp-based transcripts
* UTF-8-SIG transcript output
* Voice Activity Detection (VAD)
* Structured logging
* Rotating log files
* Error handling and validation
* Configurable Whisper model selection
* YAML-based audio file configuration with local override discovery
* Production-style modular code structure

---

# Tech Stack

* Python 3.12+
* Faster Whisper
* FFmpeg
* PyYAML
* PyCharm
* Virtual Environment (venv)

---

# Project Structure

```text
VoiceScribe/
├── app.py
├── README.md
├── pyproject.toml
├── requirements.txt
├── mock_config.yaml
├── .gitignore
├── config/
│   ├── whisper_config.py
│   └── audio_config.yaml
├── utils/
│   ├── logger.py
│   └── media_converter.py
├── audio/
├── transcripts/
├── logs/
└── summaries/
```

---

# Current Workflow

```text
Audio
 ↓
Audio Validation
 ↓
FFmpeg Conversion
 ↓
Faster Whisper
 ↓
Timestamp Formatting
 ↓
Transcript File
```

# Configuration Discovery

VoiceScribe resolves configuration in this order:

1. `--config <path>` CLI option
2. `config.yaml` or `audio_config.yaml` found in the current working folder
3. default `config/audio_config.yaml`

If a local config file exists, it is loaded automatically and used before the embedded default.
CLI flags can still override any value from that config.

# Example Config Template

A top-level `mock_config.yaml` is included as a sample configuration template.
Use it to create or copy your own `config.yaml` in the folder where you run VoiceScribe.

```yaml
selected_audio: "audio/your_audio_file.ogg"
whisper:
  model: "medium"
  device: "cpu"
  compute_type: "int8"
  language: "en"
  vad_filter: true
  beam_size: 5
summary:
  model: "qwen3:4b"
  prompt_template: |
    Analyze the meeting transcript and generate a structured summary.

    Transcript:
    {transcript}
output:
  transcripts_folder: "transcripts"
  summaries_folder: "summaries"
  logs_folder: "logs"
pipeline:
  skip_conversion: false
  skip_summary: false
ffmpeg:
  path: "ffmpeg"
logging:
  level: "INFO"
```

---

# Supported Audio Formats

```text
.aac
.mp3
.wav
.m4a
.ogg
.opus
.flac
```

---

# Future Roadmap

## Phase 1

* AI Meeting Summary
* Meeting Notes Generation
* Markdown Reports

## Phase 2

* Action Item Extraction
* Decision Tracking
* Risk Identification

## Phase 3

* Speaker Diarization
* Speaker-wise Transcripts

## Phase 4

* Local LLM Integration (Ollama)

## Phase 5

* Knowledge Base Generation
* Meeting Search
* RAG-based Transcript Retrieval

## Phase 6

* Topic Detection
* Sentiment Analysis
* Conversation Analytics
* Multi-language Intelligence

---

# Design Principles

* Offline First
* Privacy Focused
* Modular Architecture
* Reusable Components
* Minimal Dependencies
* Production-Oriented Design

```
```
