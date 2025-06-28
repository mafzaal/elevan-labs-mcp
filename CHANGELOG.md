# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md file for project version tracking

## [0.1.0] - 2025-06-28

### Added
- Initial release of ElevenLabs MCP Server
- Model Context Protocol (MCP) server implementation for ElevenLabs text-to-speech API
- Core text-to-speech functionality with `elevenlabs_text_to_speech` tool
- Voice management tools:
  - `elevenlabs_list_voices` - List all available voices from ElevenLabs account
  - `elevenlabs_get_voice_info` - Get detailed information about specific voices
- Model management with `elevenlabs_get_models` tool
- Streaming support with `elevenlabs_stream_text_to_speech` for longer texts
- Multiple audio output formats support:
  - MP3 formats: 44.1kHz/128kbps, 44.1kHz/192kbps, 44.1kHz/64kbps
  - PCM formats: 16kHz, 22.05kHz, 24kHz, 44.1kHz
  - WAV formats: 22.05kHz, 44.1kHz, 48kHz
  - μ-law 8kHz format
- Flexible voice settings configuration:
  - Stability control
  - Similarity boost
  - Style adjustment
  - Speaker boost option
- Automatic file management and smart naming
- Environment variable configuration support with `.env` file
- Comprehensive project structure with proper packaging
- Development workflow with Makefile
- CI/CD pipeline with GitHub Actions:
  - Automated testing
  - Code coverage with Codecov
  - PyPI publishing workflow
  - Dependabot dependency updates

### Technical Details
- Python 3.13+ support
- Dependencies:
  - `mcp>=1.0.0` - Model Context Protocol framework
  - `elevenlabs>=2.5.0` - ElevenLabs API integration
  - `httpx>=0.25.0` - HTTP client
  - `pydantic>=2.0.0` - Data validation
  - `python-dotenv>=1.1.1` - Environment variable management
- Development dependencies for testing and code quality
- MIT License
- Comprehensive documentation with README.md and QUICK_START.md
- Example scripts and configuration files

### Configuration
- Default voice: George (JBFqnCBsd6RMkjVDRZzb)
- Default model: eleven_multilingual_v2
- Default output format: mp3_44100_128
- Default output directory: ./audio_output
- Configurable via environment variables and function parameters

## [Links]
- [Repository](https://github.com/mafzaal/elevan-labs-mcp)
- [Documentation](https://github.com/mafzaal/elevan-labs-mcp#readme)
- [Bug Tracker](https://github.com/mafzaal/elevan-labs-mcp/issues)
- [ElevenLabs API](https://elevenlabs.io/)
