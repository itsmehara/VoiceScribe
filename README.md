# VoiceScribe
VoiceScribe is an AI-powered speech-to-text application built using OpenAI Whisper and Python for converting meeting recordings and audio conversations into accurate transcripts. It focuses on privacy-first local transcription, meeting summarization, and scalable voice intelligence workflows.

# VoiceScribe

VoiceScribe is an AI-powered speech-to-text and meeting intelligence application built using OpenAI Whisper and Python.

The project focuses on converting meeting recordings, interviews, voice notes, and conversations into structured transcripts, summaries, meeting notes, and actionable insights.

VoiceScribe is designed with a scalable architecture so it can later support advanced AI features such as:
- Meeting summarization
- MOM generation
- Speaker diarization
- AI-based action item extraction
- Keyword and topic detection
- Conversation analytics
- Local LLM integrations
- RAG-based transcript search
- Multi-language transcription

---

# Features

- Convert audio recordings into text transcripts
- Support for AAC, MP3, WAV, M4A, and other formats
- Local offline transcription using OpenAI Whisper
- Privacy-focused processing
- Multiple Whisper model support
- Subtitle generation (SRT/VTT)
- Structured transcript outputs
- Python virtual environment isolation
- Easy PyCharm integration

---

# Tech Stack

- Python 3.12+
- OpenAI Whisper
- FFmpeg
- PyCharm
- Virtual Environment (venv)

---

# Project Structure

```text
VoiceScribe/
│
├── audio/                 # Input audio files
├── transcripts/           # Generated transcripts
├── venv/                  # Python virtual environment
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── README.md
└── .gitignore
