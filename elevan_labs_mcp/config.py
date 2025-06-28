"""Configuration settings for the ElevenLabs MCP server."""

import os
from typing import Any, Dict

# Default voice settings
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.71,
    "similarity_boost": 0.5,
    "style": 0.0,
    "use_speaker_boost": True,
}

# Popular voice IDs (these are public voices available to all users)
POPULAR_VOICES = {
    "george": "JBFqnCBsd6RMkjVDRZzb",  # George - Deep, authoritative
    "rachel": "21m00Tcm4TlvDq8ikWAM",  # Rachel - Calm, pleasant
    "clyde": "2EiwWnXFnvU5JabPnv8n",  # Clyde - Warm, friendly
    "domi": "AZnzlk1XvdvUeBnXmlld",  # Domi - Strong, confident
    "dave": "CYw3kZ02Hs0563khs1Fj",  # Dave - Conversational
    "fin": "D38z5RcWu1voky8WS1ja",  # Fin - Elderly, wise
    "sarah": "EXAVITQu4vr4xnSDxMaL",  # Sarah - Soft, gentle
    "antoni": "ErXwobaYiN019PkySvjV",  # Antoni - Well-rounded
    "thomas": "GBv7mTt0atIp3Br8iCZE",  # Thomas - Calm, pleasant
    "charlie": "IKne3meq5aSn9XLyUdCD",  # Charlie - Casual, conversational
    "emily": "LcfcDJNUP1GQjkzn1xUU",  # Emily - Calm, pleasant
    "elli": "MF3mGyEYCl7XYWbV9V6O",  # Elli - Emotional, young
    "callum": "N2lVS1w4EtoT3dr4eOWO",  # Callum - Hoarse, intense
    "patrick": "ODq5zmih8GrVes37Dizd",  # Patrick - Shouty, intense
    "harry": "SOYHLrjzK2X1ezoPC6cr",  # Harry - Anxious, young
    "liam": "TX3LPaxmHKxFdv7VOQHJ",  # Liam - Articulate
    "dorothy": "ThT5KcBeYPX3keUQqHPh",  # Dorothy - Pleasant, young
}

# Output format options with descriptions
OUTPUT_FORMATS = {
    # MP3 formats
    "mp3_44100_128": "MP3, 44.1kHz, 128kbps (recommended)",
    "mp3_44100_192": "MP3, 44.1kHz, 192kbps (high quality, requires Creator+)",
    "mp3_44100_64": "MP3, 44.1kHz, 64kbps (compact)",
    # PCM formats (require Pro+)
    "pcm_16000": "PCM, 16kHz (phone quality)",
    "pcm_22050": "PCM, 22.05kHz (good quality)",
    "pcm_24000": "PCM, 24kHz (good quality)",
    "pcm_44100": "PCM, 44.1kHz (CD quality, requires Pro+)",
    # WAV formats
    "wav_22050": "WAV, 22.05kHz",
    "wav_44100": "WAV, 44.1kHz",
    "wav_48000": "WAV, 48kHz",
    # μ-law format (for telephony)
    "ulaw_8000": "μ-law, 8kHz (Twilio compatible)",
}

# Model information
MODELS_INFO = {
    "eleven_multilingual_v2": {
        "name": "Eleven Multilingual v2",
        "description": "Cutting-edge model supporting 29 languages",
        "languages": 29,
        "quality": "high",
        "speed": "medium",
    },
    "eleven_monolingual_v1": {
        "name": "Eleven Monolingual v1",
        "description": "High-quality English-only model",
        "languages": 1,
        "quality": "very_high",
        "speed": "medium",
    },
    "eleven_multilingual_v1": {
        "name": "Eleven Multilingual v1",
        "description": "Previous generation multilingual model",
        "languages": 28,
        "quality": "medium",
        "speed": "fast",
    },
    "eleven_turbo_v2": {
        "name": "Eleven Turbo v2",
        "description": "Fast, optimized for low latency",
        "languages": 32,
        "quality": "medium",
        "speed": "very_fast",
    },
    "eleven_flash_v2": {
        "name": "Eleven Flash v2",
        "description": "Ultra-fast model for real-time applications",
        "languages": 32,
        "quality": "medium",
        "speed": "ultra_fast",
    },
}


def get_config() -> Dict[str, Any]:
    """Get configuration from environment variables with defaults."""
    return {
        "api_key": os.getenv("ELEVENLABS_API_KEY"),
        "default_voice_id": os.getenv(
            "ELEVENLABS_DEFAULT_VOICE_ID", POPULAR_VOICES["george"]
        ),
        "default_model_id": os.getenv(
            "ELEVENLABS_DEFAULT_MODEL_ID", "eleven_multilingual_v2"
        ),
        "default_output_format": os.getenv(
            "ELEVENLABS_DEFAULT_OUTPUT_FORMAT", "mp3_44100_128"
        ),
        "output_directory": os.getenv("ELEVENLABS_OUTPUT_DIR", "./audio_output"),
        "max_text_length": int(os.getenv("ELEVENLABS_MAX_TEXT_LENGTH", "5000")),
        "enable_logging": os.getenv("ELEVENLABS_ENABLE_LOGGING", "true").lower()
        == "true",
    }


def validate_voice_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize voice settings."""
    validated = {}

    if "stability" in settings:
        stability = float(settings["stability"])
        validated["stability"] = max(0.0, min(1.0, stability))

    if "similarity_boost" in settings:
        similarity_boost = float(settings["similarity_boost"])
        validated["similarity_boost"] = max(0.0, min(1.0, similarity_boost))

    if "style" in settings:
        style = float(settings["style"])
        validated["style"] = max(0.0, min(1.0, style))

    if "use_speaker_boost" in settings:
        validated["use_speaker_boost"] = bool(settings["use_speaker_boost"])

    return validated


def get_voice_by_name(name: str) -> str:
    """Get voice ID by name from popular voices."""
    name_lower = name.lower()
    if name_lower in POPULAR_VOICES:
        return POPULAR_VOICES[name_lower]

    # Try partial matching
    for voice_name, voice_id in POPULAR_VOICES.items():
        if name_lower in voice_name or voice_name in name_lower:
            return voice_id

    raise ValueError(
        f"Voice '{name}' not found in popular voices. Available: {list(POPULAR_VOICES.keys())}"
    )
