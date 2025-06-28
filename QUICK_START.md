# ElevenLabs MCP Server - Quick Start Guide

## 📋 Prerequisites

1. **Python 3.13+** installed
2. **ElevenLabs API Key** - Get one from [ElevenLabs Dashboard](https://elevenlabs.io/app/speech-synthesis)

## 🚀 Quick Installation

1. **Clone/Download the project**
   ```bash
   cd /path/to/elevan-labs-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install mcp elevenlabs httpx pydantic
   ```

3. **Set your API key**
   ```bash
   export ELEVENLABS_API_KEY="your_api_key_here"
   ```
   
   Or create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

4. **Test the setup**
   ```bash
   python test_setup.py
   ```

5. **Run the server**
   ```bash
   python main.py
   ```

## 🎯 Quick Test

Run the demo to verify everything works:
```bash
python demo.py
```

## 🔧 MCP Client Configuration

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "elevenlabs-tts": {
      "command": "python",
      "args": ["/full/path/to/elevan-labs-mcp/main.py"],
      "env": {
        "ELEVENLABS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available Tools

### 1. `elevenlabs_text_to_speech`
Convert text to speech with full customization.

**Basic usage:**
```json
{
  "text": "Hello, world!"
}
```

**Advanced usage:**
```json
{
  "text": "Custom voice example",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "output_format": "mp3_44100_192",
  "voice_settings": {
    "stability": 0.75,
    "similarity_boost": 0.8
  }
}
```

### 2. `elevenlabs_list_voices`
Get all available voices from your account.

```json
{}
```

### 3. `elevenlabs_get_voice_info`
Get detailed information about a specific voice.

```json
{
  "voice_id": "JBFqnCBsd6RMkjVDRZzb"
}
```

### 4. `elevenlabs_stream_text_to_speech`
Streaming TTS for longer texts.

```json
{
  "text": "Long text content...",
  "output_file": "./my_audio.mp3"
}
```

### 5. `elevenlabs_get_models`
List all available TTS models.

```json
{}
```

## 🎵 Popular Voices

- **George** (`JBFqnCBsd6RMkjVDRZzb`) - Deep, authoritative
- **Rachel** (`21m00Tcm4TlvDq8ikWAM`) - Calm, pleasant  
- **Clyde** (`2EiwWnXFnvU5JabPnv8n`) - Warm, friendly
- **Domi** (`AZnzlk1XvdvUeBnXmlld`) - Strong, confident

## 📁 Output Formats

- `mp3_44100_128` - MP3, 44.1kHz, 128kbps (default)
- `mp3_44100_192` - MP3, 44.1kHz, 192kbps (high quality)
- `wav_44100` - WAV, 44.1kHz
- `pcm_44100` - PCM, 44.1kHz (requires Pro tier)

## ⚙️ Voice Settings

- `stability` (0-1) - Consistency between generations
- `similarity_boost` (0-1) - Similarity to original voice
- `style` (0-1) - Style amplification
- `use_speaker_boost` (true/false) - Speaker similarity boost

## 🐛 Troubleshooting

### Common Issues:

1. **"API key not set"**
   ```bash
   export ELEVENLABS_API_KEY="your_key_here"
   ```

2. **"Import errors"**
   ```bash
   pip install mcp elevenlabs httpx pydantic
   ```

3. **"Permission denied"**
   ```bash
   chmod +x start_server.sh
   ```

4. **"Voice not found"**
   - Use `elevenlabs_list_voices` to see available voices
   - Check your ElevenLabs subscription tier

### Get Help:
- Check ElevenLabs [API Documentation](https://elevenlabs.io/docs)
- Review [MCP Specification](https://github.com/modelcontextprotocol/python-sdk)

## 🎉 Ready to Use!

Your ElevenLabs MCP server is now ready. Connect it to any MCP-compatible client and start generating high-quality text-to-speech audio!
