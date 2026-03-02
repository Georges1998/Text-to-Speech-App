# Contributing to tts-app

Thanks for your interest in contributing! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/tts-app.git
   cd tts-app
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy the environment file and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```

## Making Changes

1. Create a branch for your change:
   ```bash
   git checkout -b my-feature
   ```
2. Make your changes
3. Test your changes manually:
   ```bash
   python3 tts.py voice input.txt
   python3 tts.py merge ./output
   ```
4. Commit with a clear message:
   ```bash
   git commit -m "Add feature X"
   ```
5. Push and open a pull request

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Update the README if you change CLI flags or behavior
- Add a description of what your PR does and why

## Reporting Bugs

Open an issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your Python version and OS

## Feature Requests

Open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you considered

## Code Style

- Follow existing code patterns in `tts.py`
- Use type hints for function signatures
- Keep functions focused and small
- Use `Path` from `pathlib` for file paths

## Questions?

Open an issue — we're happy to help.
