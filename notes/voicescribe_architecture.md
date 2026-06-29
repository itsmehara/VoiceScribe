# VoiceScribe Architecture and Packaging Notes

## Current System (Phase 1)

VoiceScribe is currently a deterministic, offline speech-to-text and summarization pipeline. The code flow is:

1. Audio ingestion via `config/audio_config.yaml`
2. Audio validation and conversion to WAV (`utils/media_converter.py`)
3. Whisper transcription to timestamped text (`app.py`)
4. Local LLM summary generation via Ollama (`core/summarizer.py`)
5. Files written to `transcripts/` and `summaries/`

This is a stable production-style pipeline, not an agent-based system.

## Packaging Goal

Make VoiceScribe installable as a Python package and runnable as a console script.

### What we added

- `pyproject.toml`
  - Project metadata
  - Dependencies
  - Build system (`setuptools` + `wheel`)
  - Console script entry point: `voicescribe = "app:main"`
- `requirements.txt`
  - Application dependencies for development and local install
- `config/__init__.py`, `core/__init__.py`, `utils/__init__.py`
  - Enable package discovery for wheel builds

## Recommended Architecture

### Package layout

```
voicescribe/
├── app.py
├── config/
│   ├── __init__.py
│   ├── audio_config.yaml
│   └── whisper_config.py
├── core/
│   ├── __init__.py
│   └── summarizer.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── media_converter.py
├── audio/
├── transcripts/
├── summaries/
├── logs/
├── notes/
├── pyproject.toml
└── requirements.txt
```

### Runtime model

- `app.py` is the entrypoint
- `config/whisper_config.py` is configuration and folder constants
- `utils/logger.py` handles logging and rotating file output
- `utils/media_converter.py` handles audio format conversion
- `core/summarizer.py` handles summary generation with Ollama

## Suggested Improvements for Next Evolution

### Phase 2: Config-driven execution

- Add a task configuration object or YAML file to define pipeline stages and branch selection.
- Example: `pipeline.yaml` with stages `convert`, `transcribe`, `summarize`, `export`.
- Use a lightweight executor to run stages in order or skip stages.

### Phase 3: Modular tool-based stages

- Split stages into reusable tool classes/functions.
- Example tools: `AudioConverter`, `Transcriber`, `Summarizer`, `TranscriptExporter`.
- Add a simple router that chooses tools based on file type or config.

### Phase 4: Agent-layer orchestration

- Add an agent loop for reasoning and tool selection:
  - `decide -> act -> observe -> repeat`
- Use a state object to track current artifacts and next stage.
- Keep deterministic fallback behavior for offline execution.

### Phase 5: RAG and search

- Add a local document store for transcripts and summaries.
- Use embeddings + vector search for retrieval from past meetings.
- Integrate a retriever before summarization or Q&A.

### Phase 6: Memory + meeting search

- Enhance with memory across sessions and persistent meeting knowledge.
- Add incremental indexing of transcripts and extracted decisions.

## How to build a wheel

From repo root:

```bash
/opt/homebrew/bin/python3 -m pip install --upgrade build
/opt/homebrew/bin/python3 -m build
```

This produces:

- `dist/voicescribe-0.1.0-py3-none-any.whl`
- `dist/voicescribe-0.1.0.tar.gz`

## How to install and run

Install locally:

```bash
/opt/homebrew/bin/python3 -m pip install .
```

Run the package:

```bash
voicescribe
```

## Notes and caveats

- `faster-whisper` requires local model files and may need `ctranslate2`.
- `ffmpeg` must be installed separately on the host system.
- `ollama` requires an Ollama runtime and a locally installed model.
- `config/audio_config.yaml` currently points to a static audio file name.
- This repository is not yet an agent/MCP/RAG implementation.
