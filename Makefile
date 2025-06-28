.PHONY: help install install-dev clean build test lint format check publish publish-test setup-dev check-uv

# Default target
help:
	@echo "Available targets:"
	@echo "  help         - Show this help message"
	@echo "  check-uv     - Check if uv is installed"
	@echo "  install      - Install the package"
	@echo "  install-dev  - Install the package with development dependencies"
	@echo "  setup-dev    - Set up development environment"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build the package"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  check        - Run all checks (lint, format, test)"
	@echo "  publish-test - Publish to TestPyPI"
	@echo "  publish      - Publish to PyPI"

# Check if uv is installed
check-uv:
	@command -v uv >/dev/null 2>&1 || { echo "uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }

# Installation targets
install: check-uv
	uv pip install -e .

install-dev: check-uv
	uv pip install -e .[dev]

setup-dev: install-dev
	pre-commit install

# Clean targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build targets
build: clean
	python -m build

# Testing targets
test:
	@command -v pytest >/dev/null 2>&1 || { echo "pytest not found. Run 'make install-dev' first."; exit 1; }
	pytest tests/ -v

test-cov:
	@command -v pytest >/dev/null 2>&1 || { echo "pytest not found. Run 'make install-dev' first."; exit 1; }
	pytest tests/ -v --cov=elevan_labs_mcp --cov-report=html --cov-report=term-missing

# Code quality targets
lint:
	@command -v flake8 >/dev/null 2>&1 || { echo "flake8 not found. Run 'make install-dev' first."; exit 1; }
	@command -v mypy >/dev/null 2>&1 || { echo "mypy not found. Run 'make install-dev' first."; exit 1; }
	flake8 elevan_labs_mcp/
	mypy elevan_labs_mcp/

format:
	@command -v black >/dev/null 2>&1 || { echo "black not found. Run 'make install-dev' first."; exit 1; }
	@command -v isort >/dev/null 2>&1 || { echo "isort not found. Run 'make install-dev' first."; exit 1; }
	black elevan_labs_mcp/ tests/
	isort elevan_labs_mcp/ tests/

format-check:
	@command -v black >/dev/null 2>&1 || { echo "black not found. Run 'make install-dev' first."; exit 1; }
	@command -v isort >/dev/null 2>&1 || { echo "isort not found. Run 'make install-dev' first."; exit 1; }
	black --check elevan_labs_mcp/ tests/
	isort --check-only elevan_labs_mcp/ tests/

# Combined checks
check: format-check lint test

# Publishing targets
publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

# Development server
start-server:
	python -m elevan_labs_mcp.server

# Install build dependencies
install-build-deps: check-uv
	uv pip install build twine

# Full development setup
dev-setup: install-build-deps install-dev setup-dev
	@echo "Development environment set up successfully!"
	@echo "Run 'make help' to see available commands."
