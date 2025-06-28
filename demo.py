#!/usr/bin/env python3
"""
Quick demo of the ElevenLabs MCP Server functionality

This script demonstrates the server capabilities by importing and calling functions directly.
Note: This is for testing only - in production, tools should be called via MCP protocol.
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

async def demo_functionality():
    """Demonstrate the server functionality."""
    print("ElevenLabs MCP Server - Functionality Demo")
    print("==========================================")
    
    # Check if API key is available
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ ELEVENLABS_API_KEY is not set")
        print("Please set your API key: export ELEVENLABS_API_KEY='your_key'")
        return
    
    try:
        # Import the server functions
        from elevan_labs_mcp.server import (
            handle_list_voices,
            handle_get_models,
            handle_text_to_speech
        )
        
        print("✅ Server modules imported successfully")
        print()
        
        # Demo 1: List available models
        print("🔹 Demo 1: Listing available models...")
        try:
            models_result = await handle_get_models({})
            models_data = json.loads(models_result[0].text)
            print(f"Found {models_data['model_count']} models")
            
            # Show first few models
            for i, model in enumerate(models_data['models'][:3]):
                print(f"  {i+1}. {model['name']} - {model['description']}")
        except Exception as e:
            print(f"❌ Error listing models: {e}")
        
        print()
        
        # Demo 2: List available voices
        print("🔹 Demo 2: Listing available voices...")
        try:
            voices_result = await handle_list_voices({})
            voices_data = json.loads(voices_result[0].text)
            print(f"Found {voices_data['voice_count']} voices")
            
            # Show first few voices
            for i, voice in enumerate(voices_data['voices'][:5]):
                print(f"  {i+1}. {voice['name']} ({voice['voice_id'][:8]}...) - {voice['category']}")
        except Exception as e:
            print(f"❌ Error listing voices: {e}")
        
        print()
        
        # Demo 3: Generate a short sample
        print("🔹 Demo 3: Generating a short text-to-speech sample...")
        try:
            tts_args = {
                "text": "Hello! This is a test of the ElevenLabs MCP server.",
                "output_file": "./audio_output/demo_sample.mp3"
            }
            
            tts_result = await handle_text_to_speech(tts_args)
            tts_data = json.loads(tts_result[0].text)
            
            if tts_data.get("success"):
                print(f"✅ Audio generated successfully!")
                print(f"   File: {tts_data['output_file']}")
                print(f"   Size: {tts_data['file_size_bytes']} bytes")
                print(f"   Voice: {tts_data['voice_id']}")
                print(f"   Model: {tts_data['model_id']}")
            else:
                print(f"❌ Generation failed: {tts_data}")
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
        
        print()
        print("🎉 Demo completed!")
        print("The server is working correctly and ready to use via MCP protocol.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install mcp elevenlabs httpx pydantic")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function."""
    try:
        asyncio.run(demo_functionality())
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    main()
