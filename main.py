"""
Alex — Nepal RAG Voice Assistant
=================================
FastAPI backend that wires together:
  • A local RAG engine (rag_engine.RAGEngine)
  • Groq Whisper for speech-to-text
  • Groq Orpheus TTS for text-to-speech
  • Simple in-memory conversation history (single-user / demo mode)

Run with:
    uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from rag_engine import RAGEngine

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("alex")

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

STT_MODEL   = "whisper-large-v3"
TTS_MODEL   = "canopylabs/orpheus-v1-english"
TTS_VOICE   = "troy"

# Knowledge-base text file (try both names for compatibility)
_SAMPLE_CANDIDATES = [BASE_DIR / "sample_text.txt", BASE_DIR / "sample.txt"]
SAMPLE_PATH: Optional[Path] = next(
    (p for p in _SAMPLE_CANDIDATES if p.exists()), None
)
SAMPLE_TEXT: str = SAMPLE_PATH.read_text(encoding="utf-8").strip() if SAMPLE_PATH else ""

if SAMPLE_TEXT:
    log.info("Knowledge base loaded: %s (%d chars)", SAMPLE_PATH.name, len(SAMPLE_TEXT))
else:
    log.warning("No knowledge-base file found — RAG context will be empty.")

TTS_OUTPUT_PATH = Path(tempfile.gettempdir()) / "alex_response.wav"
STATIC_DIR      = BASE_DIR / "static"
INDEX_HTML      = BASE_DIR / "index.html"

# ──────────────────────────────────────────────
# App
# ──────────────────────────────────────────────
app = FastAPI(
    title="Alex — Nepal RAG Voice Assistant",
    description="AI guide to Nepal powered by a local knowledge base, Groq STT/TTS, and RAGEngine.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (optional; skip if folder absent)
if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ── Shared state ──────────────────────────────
engine: RAGEngine = RAGEngine()
conversation_history: list[dict] = []

# ──────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User message text")


class ChatResponse(BaseModel):
    answer: str


class VoiceChatResponse(BaseModel):
    transcript: str
    answer: str
    audio_url: Optional[str] = None


class ResetResponse(BaseModel):
    status: str
    messages_cleared: int


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _build_rag_prompt(user_input: str) -> str:
    """Inject the knowledge-base context around the user question."""
    if not SAMPLE_TEXT:
        return user_input
    return (
        f"User question:\n{user_input}\n\n"
        f"Reference text from knowledge base:\n{SAMPLE_TEXT}"
    )


def _append_history(role: str, content: str) -> None:
    conversation_history.append({"role": role, "content": content})


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, summary="Serve the chat UI")
def serve_frontend() -> str:
    if not INDEX_HTML.exists():
        raise HTTPException(status_code=404, detail="index.html not found.")
    return INDEX_HTML.read_text(encoding="utf-8")


@app.get("/health", summary="Health check")
def health() -> dict:
    """Returns service health and basic stats."""
    return {
        "status": "ok",
        "knowledge_base": bool(SAMPLE_TEXT),
        "history_length": len(conversation_history),
    }


@app.post("/chat", response_model=ChatResponse, summary="Text chat with RAG")
def chat(request: ChatRequest) -> ChatResponse:
    """
    Accept a plain-text message, run it through the RAG engine with
    conversation history, and return the assistant's answer.
    """
    log.info("Chat │ user: %.80s…", request.message)

    prompt = _build_rag_prompt(request.message)
    answer = engine.chat(prompt, conversation_history)

    _append_history("user", request.message)
    _append_history("assistant", answer)

    log.info("Chat │ answer: %.80s…", answer)
    return ChatResponse(answer=answer)


@app.post("/voice-chat", response_model=VoiceChatResponse, summary="Voice chat (STT → RAG → TTS)")
async def voice_chat(audio: UploadFile = File(...)) -> VoiceChatResponse:
    """
    Full voice pipeline:
      1. Upload an audio blob (webm / wav / mp3).
      2. Transcribe with Groq Whisper.
      3. Answer with RAG engine.
      4. Synthesize reply with Groq Orpheus TTS.
      5. Return transcript, answer text, and audio URL.
    """
    suffix = os.path.splitext(audio.filename or "")[1] or ".webm"

    # ── 1. Save upload to temp file ──────────────────
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    # ── 2. Transcribe ────────────────────────────────
    try:
        with open(tmp_path, "rb") as f:
            transcription = engine.client.audio.transcriptions.create(
                file=f,
                model=STT_MODEL,
            )
        user_text = transcription.text.strip()
        log.info("Voice │ transcript: %.80s…", user_text)
    except Exception as exc:
        log.exception("Voice │ STT failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {exc}") from exc
    finally:
        os.remove(tmp_path)

    if not user_text:
        return VoiceChatResponse(
            transcript="",
            answer="I didn't catch any speech — please try again.",
            audio_url=None,
        )

    # ── 3. RAG answer ────────────────────────────────
    answer = engine.chat(_build_rag_prompt(user_text), conversation_history)
    _append_history("user", user_text)
    _append_history("assistant", answer)

    # ── 4. TTS synthesis ─────────────────────────────
    audio_url: Optional[str] = None
    try:
        speech = engine.client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=answer,
            response_format="wav",
        )
        speech.write_to_file(str(TTS_OUTPUT_PATH))
        audio_url = "/audio-response"
        log.info("Voice │ TTS written to %s", TTS_OUTPUT_PATH)
    except Exception as exc:
        # Non-fatal — we still return the text answer
        log.warning("Voice │ TTS failed (non-fatal): %s", exc)

    return VoiceChatResponse(transcript=user_text, answer=answer, audio_url=audio_url)


@app.get("/audio-response", summary="Stream the latest TTS audio")
def audio_response() -> FileResponse:
    if not TTS_OUTPUT_PATH.exists():
        raise HTTPException(status_code=404, detail="No audio response available yet.")
    return FileResponse(str(TTS_OUTPUT_PATH), media_type="audio/wav")


@app.post("/reset", response_model=ResetResponse, summary="Clear conversation history")
def reset() -> ResetResponse:
    cleared = len(conversation_history)
    conversation_history.clear()
    log.info("Conversation reset (%d messages cleared)", cleared)
    return ResetResponse(status="conversation reset", messages_cleared=cleared)