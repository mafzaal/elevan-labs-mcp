# ElevenLabs MCP Server

A Model Context Protocol (MCP) server that provides text-to-speech functionality using the ElevenLabs API. This server allows you to convert text to natural-sounding speech with various voices and models.

## Features

- **Text-to-Speech Conversion**: Convert any text to high-quality speech
- **Voice Management**: List and get detailed information about available voices
- **Multiple Models**: Support for various ElevenLabs TTS models
- **Streaming Support**: Real-time audio generation for longer texts
- **Flexible Output**: Multiple audio formats and custom voice settings
- **Automatic File Management**: Smart file naming and directory creation

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd elevan-labs-mcp
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up your ElevenLabs API key:
```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

Or create a `.env` file in the project root:
```bash
cp .env.example .env
# Edit .env and add your API key
```

You can get your API key from [ElevenLabs Dashboard](https://elevenlabs.io/app/speech-synthesis).

## Usage

### Running the Server

```bash
python main.py
```

Or using the installed script:
```bash
elevan-labs-mcp
```

## 🤖 LLM Integration

### MCP Configuration

The `mcp.json` file provides configuration with clients:

```json
{
    "servers": {
        "elevenlabs-mcp": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "--directory",
                "${workspaceFolder}",
                "elevan-labs-mcp"
                
            ],
            "envFile": "${workspaceFolder}/.env"
        }
    }
}
```

### Available Tools

#### 1. `elevenlabs_text_to_speech`
Convert text to speech with extensive customization options.

**Parameters:**
- `text` (required): The text to convert to speech
- `voice_id` (optional): Voice ID to use (defaults to George voice)
- `model_id` (optional): Model to use (defaults to eleven_multilingual_v2)
- `output_format` (optional): Audio format (defaults to mp3_44100_128)
- `output_file` (optional): Custom output file path
- `voice_settings` (optional): Custom voice settings (stability, similarity_boost, etc.)

**Example:**
```json
{
  "text": "Hello, this is a test of the ElevenLabs text-to-speech API.",
  "voice_id": "JBFqnCBsd6RMkjVDRZzb",
  "output_format": "mp3_44100_128"
}
```

#### 2. `elevenlabs_list_voices`
Get all available voices from your ElevenLabs account.

**Parameters:** None

**Returns:** List of voices with their IDs, names, categories, and settings.

#### 3. `elevenlabs_get_voice_info`
Get detailed information about a specific voice.

**Parameters:**
- `voice_id` (required): ID of the voice to query

**Returns:** Detailed voice information including samples and settings.

#### 4. `elevenlabs_stream_text_to_speech`
Convert text to speech with streaming for real-time generation.

**Parameters:**
- `text` (required): The text to convert
- `voice_id` (optional): Voice ID to use
- `model_id` (optional): Model to use
- `output_file` (required): Output file path

#### 5. `elevenlabs_get_models`
Get all available text-to-speech models.

**Parameters:** None

**Returns:** List of models with their capabilities and limitations.

## Supported Audio Formats

- MP3: `mp3_44100_128`, `mp3_44100_192`, `mp3_44100_64`
- PCM: `pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_44100`
- WAV: `wav_22050`, `wav_44100`, `wav_48000`
- μ-law: `ulaw_8000`

## Voice Settings

You can customize voice generation with these settings:

- `stability` (0-1): Controls consistency between generations
- `similarity_boost` (0-1): Enhances similarity to the original voice
- `style` (0-1): Amplifies the style of the original speaker
- `use_speaker_boost` (boolean): Boost similarity to the original speaker

## Error Handling

The server includes comprehensive error handling for:
- Missing API keys
- Invalid voice IDs
- API rate limits
- Network issues
- File system errors

## Configuration

### Environment Variables

- `ELEVENLABS_API_KEY`: Your ElevenLabs API key (required)

### Default Settings

- Default Voice: George (`JBFqnCBsd6RMkjVDRZzb`)
- Default Model: `eleven_multilingual_v2`
- Default Format: `mp3_44100_128`
- Default Output Directory: `./audio_output`

## Examples

### Basic Text-to-Speech

```json
{
  "tool": "elevenlabs_text_to_speech",
  "arguments": {
    "text": "Welcome to the ElevenLabs MCP server!"
  }
}
```

### Custom Voice and Settings

```json
{
  "tool": "elevenlabs_text_to_speech",
  "arguments": {
    "text": "This is a custom voice example.",
    "voice_id": "your_voice_id_here",
    "voice_settings": {
      "stability": 0.75,
      "similarity_boost": 0.8,
      "style": 0.6
    }
  }
}
```

### List Available Voices

```json
{
  "tool": "elevenlabs_list_voices",
  "arguments": {}
}
```

## Development

### Project Structure

```
elevan-labs-mcp/
├── elevan_labs_mcp/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

### Dependencies

- `mcp>=1.0.0`: Model Context Protocol SDK
- `elevenlabs>=1.0.0`: ElevenLabs Python SDK
- `httpx>=0.25.0`: HTTP client
- `pydantic>=2.0.0`: Data validation

## Troubleshooting

### Common Issues

1. **Missing API Key**: Make sure `ELEVENLABS_API_KEY` is set in your environment
2. **Voice Not Found**: Use `elevenlabs_list_voices` to see available voices
3. **Rate Limits**: ElevenLabs has rate limits based on your subscription tier
4. **File Permissions**: Ensure the output directory is writable

### Getting Help

- Check the [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- Review the [MCP Specification](https://github.com/modelcontextprotocol/python-sdk)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.