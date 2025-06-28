#!/usr/bin/env python3
"""
Example usage of the ElevenLabs MCP Server

This script demonstrates how to use the various tools provided by the server.
Make sure the server is running and your API key is set before running this.
"""

import json
import asyncio
from typing import Dict, Any

# Example tool calls for demonstration
EXAMPLE_CALLS = [
    {
        "name": "elevenlabs_list_voices",
        "description": "List all available voices",
        "arguments": {}
    },
    {
        "name": "elevenlabs_get_models", 
        "description": "Get all available TTS models",
        "arguments": {}
    },
    {
        "name": "elevenlabs_text_to_speech",
        "description": "Basic text-to-speech conversion",
        "arguments": {
            "text": "Hello! This is a test of the ElevenLabs text-to-speech functionality through the MCP server."
        }
    },
    {
        "name": "elevenlabs_text_to_speech",
        "description": "Text-to-speech with custom voice and settings",
        "arguments": {
            "text": "This example uses custom voice settings for a more personalized output.",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            "output_format": "mp3_44100_192",
            "voice_settings": {
                "stability": 0.8,
                "similarity_boost": 0.7,
                "style": 0.2,
                "use_speaker_boost": True
            }
        }
    },
    {
        "name": "elevenlabs_get_voice_info",
        "description": "Get detailed information about George voice",
        "arguments": {
            "voice_id": "JBFqnCBsd6RMkjVDRZzb"
        }
    },
    {
        "name": "elevenlabs_stream_text_to_speech",
        "description": "Streaming text-to-speech for longer content",
        "arguments": {
            "text": "This is a longer piece of text that demonstrates the streaming capabilities of the ElevenLabs API. Streaming is particularly useful for real-time applications or when working with longer content that needs to be processed efficiently.",
            "output_file": "./audio_output/streaming_example.mp3"
        }
    }
]

def print_example_call(call: Dict[str, Any]) -> None:
    """Print a formatted example call."""
    print(f"\n{'='*60}")
    print(f"Tool: {call['name']}")
    print(f"Description: {call['description']}")
    print(f"Arguments:")
    print(json.dumps(call['arguments'], indent=2))
    print(f"{'='*60}")

def main():
    """Main function to display example usage."""
    print("ElevenLabs MCP Server - Example Usage")
    print("====================================")
    
    print("\nThis script shows example tool calls for the ElevenLabs MCP server.")
    print("To actually use these tools, you need to:")
    print("1. Start the MCP server: python main.py")
    print("2. Connect an MCP client to the server") 
    print("3. Call the tools through the MCP protocol")
    
    print(f"\nAvailable Tools ({len(EXAMPLE_CALLS)} examples):")
    
    for i, call in enumerate(EXAMPLE_CALLS, 1):
        print(f"\n{i}. {call['name']}")
        print(f"   {call['description']}")
    
    print("\nDetailed Examples:")
    
    for call in EXAMPLE_CALLS:
        print_example_call(call)
    
    print("\nEnvironment Setup:")
    print("export ELEVENLABS_API_KEY='your_api_key_here'")
    
    print("\nCommon Voice IDs:")
    popular_voices = {
        "george": "JBFqnCBsd6RMkjVDRZzb",
        "rachel": "21m00Tcm4TlvDq8ikWAM", 
        "clyde": "2EiwWnXFnvU5JabPnv8n",
        "domi": "AZnzlk1XvdvUeBnXmlld"
    }
    
    for name, voice_id in popular_voices.items():
        print(f"  {name.capitalize()}: {voice_id}")
    
    print("\nSupported Output Formats:")
    formats = [
        "mp3_44100_128 (default)",
        "mp3_44100_192 (high quality)",
        "wav_44100",
        "pcm_44100"
    ]
    
    for fmt in formats:
        print(f"  - {fmt}")

if __name__ == "__main__":
    main()
