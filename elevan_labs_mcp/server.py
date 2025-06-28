#!/usr/bin/env python3
"""
ElevenLabs MCP Server

This server provides Model Context Protocol (MCP) tools for text-to-speech
functionality using the ElevenLabs API.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from mcp.server import Server
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    Resource,
    TextContent,
    Tool,
)
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("elevenlabs-mcp")

# Global ElevenLabs client
elevenlabs_client: Optional[ElevenLabs] = None

# Default configuration
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # George voice
DEFAULT_MODEL_ID = "eleven_multilingual_v2"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_OUTPUT_DIR = "./audio_output"


class VoiceSettings(BaseModel):
    """Voice settings configuration."""

    stability: Optional[float] = None
    similarity_boost: Optional[float] = None
    style: Optional[float] = None
    use_speaker_boost: Optional[bool] = None


def get_elevenlabs_client() -> ElevenLabs:
    """Get or create ElevenLabs client."""
    global elevenlabs_client

    if elevenlabs_client is None:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError(
                "ELEVENLABS_API_KEY environment variable is required. "
                "Please set it with your ElevenLabs API key."
            )
        elevenlabs_client = ElevenLabs(api_key=api_key)

    return elevenlabs_client


def ensure_output_directory(output_path: str) -> Path:
    """Ensure output directory exists and return Path object."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def generate_output_filename(text: str, voice_id: str, output_format: str) -> str:
    """Generate a descriptive filename for the output audio."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean text for filename (first 30 chars, replace spaces/special chars)
    clean_text = "".join(
        c for c in text[:30] if c.isalnum() or c in (" ", "-", "_")
    ).strip()
    clean_text = clean_text.replace(" ", "_")

    # Extract file extension from format
    if output_format.startswith("mp3"):
        ext = "mp3"
    elif output_format.startswith("wav"):
        ext = "wav"
    elif output_format.startswith("pcm"):
        ext = "pcm"
    else:
        ext = "mp3"  # default

    return f"{clean_text}_{voice_id[:8]}_{timestamp}.{ext}"


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="elevenlabs_text_to_speech",
            description="Convert text to speech using ElevenLabs API",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to convert to speech",
                    },
                    "voice_id": {
                        "type": "string",
                        "description": f"ID of the voice to use (default: {DEFAULT_VOICE_ID})",
                        "default": DEFAULT_VOICE_ID,
                    },
                    "model_id": {
                        "type": "string",
                        "description": f"Model to use for generation (default: {DEFAULT_MODEL_ID})",
                        "default": DEFAULT_MODEL_ID,
                    },
                    "output_format": {
                        "type": "string",
                        "description": f"Audio output format (default: {DEFAULT_OUTPUT_FORMAT})",
                        "default": DEFAULT_OUTPUT_FORMAT,
                        "enum": [
                            "mp3_44100_128",
                            "mp3_44100_192",
                            "mp3_44100_64",
                            "pcm_16000",
                            "pcm_22050",
                            "pcm_24000",
                            "pcm_44100",
                            "ulaw_8000",
                            "wav_22050",
                            "wav_44100",
                            "wav_48000",
                        ],
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Custom output file path (optional, auto-generated if not provided)",
                    },
                    "voice_settings": {
                        "type": "object",
                        "description": "Custom voice settings",
                        "properties": {
                            "stability": {"type": "number", "minimum": 0, "maximum": 1},
                            "similarity_boost": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                            },
                            "style": {"type": "number", "minimum": 0, "maximum": 1},
                            "use_speaker_boost": {"type": "boolean"},
                        },
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="elevenlabs_list_voices",
            description="Get all available voices from your ElevenLabs account",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="elevenlabs_get_voice_info",
            description="Get detailed information about a specific voice",
            inputSchema={
                "type": "object",
                "properties": {
                    "voice_id": {
                        "type": "string",
                        "description": "ID of the voice to get information about",
                    },
                },
                "required": ["voice_id"],
            },
        ),
        Tool(
            name="elevenlabs_stream_text_to_speech",
            description="Convert text to speech with streaming (for longer texts or real-time generation)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to convert to speech",
                    },
                    "voice_id": {
                        "type": "string",
                        "description": f"ID of the voice to use (default: {DEFAULT_VOICE_ID})",
                        "default": DEFAULT_VOICE_ID,
                    },
                    "model_id": {
                        "type": "string",
                        "description": f"Model to use for generation (default: {DEFAULT_MODEL_ID})",
                        "default": DEFAULT_MODEL_ID,
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Output file path for the streamed audio",
                    },
                },
                "required": ["text", "output_file"],
            },
        ),
        Tool(
            name="elevenlabs_get_models",
            description="Get all available text-to-speech models",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "elevenlabs_text_to_speech":
            return await handle_text_to_speech(arguments)
        elif name == "elevenlabs_list_voices":
            return await handle_list_voices(arguments)
        elif name == "elevenlabs_get_voice_info":
            return await handle_get_voice_info(arguments)
        elif name == "elevenlabs_stream_text_to_speech":
            return await handle_stream_text_to_speech(arguments)
        elif name == "elevenlabs_get_models":
            return await handle_get_models(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error in {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_text_to_speech(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle text-to-speech conversion."""
    text = arguments["text"]
    voice_id = arguments.get("voice_id", DEFAULT_VOICE_ID)
    model_id = arguments.get("model_id", DEFAULT_MODEL_ID)
    output_format = arguments.get("output_format", DEFAULT_OUTPUT_FORMAT)
    output_file = arguments.get("output_file")
    voice_settings_dict = arguments.get("voice_settings")

    client = get_elevenlabs_client()

    # Generate output file path if not provided
    if not output_file:
        filename = generate_output_filename(text, voice_id, output_format)
        output_file = os.path.join(DEFAULT_OUTPUT_DIR, filename)

    output_path = ensure_output_directory(output_file)

    # Prepare voice settings
    voice_settings = None
    if voice_settings_dict:
        voice_settings = voice_settings_dict

    try:
        # Call ElevenLabs API
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=model_id,
            output_format=output_format,
            voice_settings=voice_settings,
        )

        # Save audio to file
        with open(output_path, "wb") as audio_file:
            for chunk in audio_generator:
                audio_file.write(chunk)

        file_size = output_path.stat().st_size

        result = {
            "success": True,
            "message": f"Successfully converted text to speech",
            "output_file": str(output_path),
            "file_size_bytes": file_size,
            "voice_id": voice_id,
            "model_id": model_id,
            "output_format": output_format,
            "text_length": len(text),
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        error_msg = f"Failed to convert text to speech: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]


async def handle_list_voices(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle listing available voices."""
    client = get_elevenlabs_client()

    try:
        voices_response = client.voices.get_all()
        voices = voices_response.voices

        result = {
            "success": True,
            "voice_count": len(voices),
            "voices": [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category,
                    "description": voice.description,
                    "preview_url": voice.preview_url,
                    "available_for_tiers": voice.available_for_tiers,
                    "settings": (
                        {
                            "stability": (
                                voice.settings.stability if voice.settings else None
                            ),
                            "similarity_boost": (
                                voice.settings.similarity_boost
                                if voice.settings
                                else None
                            ),
                            "style": voice.settings.style if voice.settings else None,
                            "use_speaker_boost": (
                                voice.settings.use_speaker_boost
                                if voice.settings
                                else None
                            ),
                        }
                        if voice.settings
                        else None
                    ),
                }
                for voice in voices
            ],
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        error_msg = f"Failed to list voices: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]


async def handle_get_voice_info(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle getting voice information."""
    voice_id = arguments["voice_id"]
    client = get_elevenlabs_client()

    try:
        voice = client.voices.get(voice_id)

        result = {
            "success": True,
            "voice": {
                "voice_id": voice.voice_id,
                "name": voice.name,
                "category": voice.category,
                "description": voice.description,
                "preview_url": voice.preview_url,
                "available_for_tiers": voice.available_for_tiers,
                "settings": (
                    {
                        "stability": (
                            voice.settings.stability if voice.settings else None
                        ),
                        "similarity_boost": (
                            voice.settings.similarity_boost if voice.settings else None
                        ),
                        "style": voice.settings.style if voice.settings else None,
                        "use_speaker_boost": (
                            voice.settings.use_speaker_boost if voice.settings else None
                        ),
                    }
                    if voice.settings
                    else None
                ),
                "samples": [
                    {
                        "sample_id": sample.sample_id,
                        "file_name": sample.file_name,
                        "mime_type": sample.mime_type,
                        "size_bytes": sample.size_bytes,
                        "hash": sample.hash,
                    }
                    for sample in (voice.samples or [])
                ],
            },
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        error_msg = f"Failed to get voice info: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]


async def handle_stream_text_to_speech(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle streaming text-to-speech conversion."""
    text = arguments["text"]
    voice_id = arguments.get("voice_id", DEFAULT_VOICE_ID)
    model_id = arguments.get("model_id", DEFAULT_MODEL_ID)
    output_file = arguments["output_file"]

    client = get_elevenlabs_client()
    output_path = ensure_output_directory(output_file)

    try:
        # Use streaming API
        audio_stream = client.text_to_speech.convert_as_stream(
            voice_id=voice_id,
            text=text,
            model_id=model_id,
        )

        # Save streamed audio to file
        with open(output_path, "wb") as audio_file:
            for chunk in audio_stream:
                audio_file.write(chunk)

        file_size = output_path.stat().st_size

        result = {
            "success": True,
            "message": f"Successfully streamed text to speech",
            "output_file": str(output_path),
            "file_size_bytes": file_size,
            "voice_id": voice_id,
            "model_id": model_id,
            "text_length": len(text),
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        error_msg = f"Failed to stream text to speech: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]


async def handle_get_models(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle getting available models."""
    client = get_elevenlabs_client()

    try:
        models_response = client.models.get_all()
        models = models_response.models

        result = {
            "success": True,
            "model_count": len(models),
            "models": [
                {
                    "model_id": model.model_id,
                    "name": model.name,
                    "can_be_finetuned": model.can_be_finetuned,
                    "can_do_text_to_speech": model.can_do_text_to_speech,
                    "can_do_voice_conversion": model.can_do_voice_conversion,
                    "token_cost_factor": model.token_cost_factor,
                    "description": model.description,
                    "requires_alpha_access": model.requires_alpha_access,
                    "max_characters_request_free_tier": model.max_characters_request_free_tier,
                    "max_characters_request_subscribed_tier": model.max_characters_request_subscribed_tier,
                    "maximum_text_length_per_request": model.maximum_text_length_per_request,
                    "languages": model.languages,
                }
                for model in models
            ],
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        error_msg = f"Failed to get models: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]


def main():
    """Main entry point for the server."""
    import mcp.server.stdio

    async def run_server():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
