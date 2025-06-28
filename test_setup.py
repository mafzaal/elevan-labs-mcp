#!/usr/bin/env python3
"""
Test script for the ElevenLabs MCP Server

This script performs basic validation of the server setup.
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 13:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires >= 3.13)")
        return False

def check_dependencies():
    """Check if required dependencies are available."""
    print("\nChecking dependencies...")
    dependencies = [
        "mcp",
        "elevenlabs", 
        "httpx",
        "pydantic"
    ]
    
    all_good = True
    for dep in dependencies:
        try:
            spec = importlib.util.find_spec(dep)
            if spec is not None:
                print(f"✓ {dep} is installed")
            else:
                print(f"✗ {dep} is not installed")
                all_good = False
        except ImportError:
            print(f"✗ {dep} is not installed")
            all_good = False
    
    return all_good

def check_api_key():
    """Check if ElevenLabs API key is set."""
    print("\nChecking API key...")
    
    # Try to load from .env file first
    env_file = Path(".env")
    if env_file.exists():
        print(f"✓ .env file found")
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            print("✗ python-dotenv not installed, cannot load .env file")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if api_key:
        # Don't print the actual key for security
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        print(f"✓ ELEVENLABS_API_KEY is set ({masked_key})")
        return True
    else:
        print("✗ ELEVENLABS_API_KEY is not set")
        print("  Option 1: Set environment variable: export ELEVENLABS_API_KEY='your_api_key_here'")
        print("  Option 2: Create .env file: cp .env.example .env (then edit with your key)")
        return False

def check_project_structure():
    """Check if project files are in place."""
    print("\nChecking project structure...")
    
    required_files = [
        "elevan_labs_mcp/__init__.py",
        "elevan_labs_mcp/server.py",
        "elevan_labs_mcp/config.py",
        "main.py",
        "pyproject.toml",
        "README.md",
        ".env.example"
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            all_good = False
    
    return all_good

def check_output_directory():
    """Check if output directory can be created."""
    print("\nChecking output directory...")
    try:
        output_dir = Path("./audio_output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Try to create a test file
        test_file = output_dir / "test_write.tmp"
        test_file.write_text("test")
        test_file.unlink()  # Remove test file
        
        print(f"✓ Output directory is writable: {output_dir.absolute()}")
        return True
    except Exception as e:
        print(f"✗ Cannot create/write to output directory: {e}")
        return False

def test_server_import():
    """Test if the server module can be imported."""
    print("\nTesting server import...")
    try:
        from elevan_labs_mcp.server import main
        print("✓ Server module imports successfully")
        return True
    except ImportError as e:
        print(f"✗ Cannot import server module: {e}")
        return False
    except Exception as e:
        print(f"✗ Error importing server module: {e}")
        return False

def main():
    """Run all tests."""
    print("ElevenLabs MCP Server - Setup Validation")
    print("========================================")
    
    tests = [
        check_python_version,
        check_project_structure,
        check_dependencies,
        check_api_key,
        check_output_directory,
        test_server_import
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*50)
    print("Test Summary:")
    print("="*50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All tests passed ({passed}/{total})")
        print("\nYou're ready to run the server!")
        print("Start with: python main.py")
    else:
        print(f"✗ {total - passed} test(s) failed ({passed}/{total} passed)")
        print("\nPlease fix the issues above before running the server.")
    
    print("\nNext Steps:")
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("1. Get your API key from: https://elevenlabs.io/app/speech-synthesis")
        print("2. Set the environment variable: export ELEVENLABS_API_KEY='your_key'")
    
    if passed < total:
        print("3. Install missing dependencies: pip install -e .")
    
    print("4. Run the server: python main.py")
    print("5. Test with examples: python examples.py")

if __name__ == "__main__":
    main()
