#!/bin/bash
"""
ElevenLabs MCP Server Startup Script

This script helps you set up and run the ElevenLabs MCP server.
"""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "ElevenLabs MCP Server Setup"
echo "==========================="

# Check if API key is set
if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo -e "${RED}Error: ELEVENLABS_API_KEY is not set${NC}"
    echo "Please set your ElevenLabs API key:"
    echo "  Option 1: export ELEVENLABS_API_KEY='your_api_key_here'"
    echo "  Option 2: Create .env file: cp .env.example .env (then edit with your key)"
    echo ""
    echo "You can get your API key from: https://elevenlabs.io/app/speech-synthesis"
    echo ""
    
    # Check if .env.example exists and offer to create .env
    if [ -f ".env.example" ] && [ ! -f ".env" ]; then
        read -p "Create .env file from template? (y/n): " create_env
        if [ "$create_env" = "y" ] || [ "$create_env" = "Y" ]; then
            cp .env.example .env
            echo -e "${GREEN}.env file created. Please edit it and add your API key.${NC}"
            echo "Then run this script again."
            exit 0
        fi
    fi
    
    read -p "Enter your ElevenLabs API key: " api_key
    if [ -n "$api_key" ]; then
        export ELEVENLABS_API_KEY="$api_key"
        echo -e "${GREEN}API key set for this session${NC}"
    else
        echo -e "${RED}No API key provided. Exiting.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ ELEVENLABS_API_KEY is set${NC}"
fi

# Run validation
echo ""
echo "Running setup validation..."
python test_setup.py

# If validation passes, offer to start the server
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}Setup validation passed!${NC}"
    echo ""
    read -p "Start the MCP server now? (y/n): " start_server
    
    if [ "$start_server" = "y" ] || [ "$start_server" = "Y" ]; then
        echo ""
        echo "Starting ElevenLabs MCP Server..."
        echo "Press Ctrl+C to stop the server"
        echo ""
        python main.py
    else
        echo "To start the server manually, run: python main.py"
    fi
else
    echo -e "${YELLOW}Please fix the validation issues before running the server.${NC}"
fi
