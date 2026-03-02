# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python CLI that converts text to speech using OpenAI's TTS API and merges audio files. Single-file application (`tts.py`) with YAML-based configuration. Two subcommands: `voice` (text-to-speech) and `merge` (combine audio files).

## Setup & Running

```bash
pip install -r requirements.txt      # Install dependencies (openai, python-dotenv, pyyaml)
cp .env.example .env                 # Then add your OPENAI_API_KEY
python3 tts.py voice input.txt       # Convert text file to speech
python3 tts.py merge ./output        # Merge audio files in a folder
```

There are no tests, linting, or build steps configured.

## CLI Subcommands

### `voice` — Convert a text file to speech
```bash
python3 tts.py voice <file> [--voice VOICE] [--model MODEL] [--format FORMAT] [--output PATH] [--output-dir DIR] [--instructions TEXT]
```
- Positional arg: path to a text file
- Defaults come from `config.yaml`; CLI flags override them
- Output goes to `./output/speech_YYYYMMDD_HHMMSS.{format}` unless `-o` is specified

### `merge` — Merge audio files alphabetically
```bash
python3 tts.py merge <folder> [--output PATH] [--format FORMAT]
```
- Positional arg: folder containing audio files
- Sorts files alphabetically and concatenates them
- Defaults to merging `.mp3` files; output is `<folder>/merged.<format>`
- Excludes the output file itself from the merge

## Architecture

All logic lives in `tts.py` with these key functions:
- `load_config()` — reads `config.yaml` defaults
- `validate_options()` — checks model/voice/format combinations
- `generate_speech()` — calls OpenAI API with streaming response, writes audio to file
- `cmd_voice()` — handles the `voice` subcommand (reads text file, resolves options, calls `generate_speech`)
- `cmd_merge()` — handles the `merge` subcommand (lists folder, sorts, concatenates binary)
- `main()` — argparse CLI with `voice` and `merge` subparsers

**Configuration hierarchy**: `config.yaml` defaults → CLI flags override → API key from `.env`

## Key Constraints

- Style instructions (`--instructions`) only work with the `gpt-4o-mini-tts` model
- Voices `ballad`, `verse`, `marin`, `cedar` are exclusive to `gpt-4o-mini-tts`; other models only support the 9 basic voices
- Audio files go to `./output/` by default with pattern `speech_YYYYMMDD_HHMMSS.{format}`
- The OpenAI client is instantiated per call in `generate_speech()` (reads `OPENAI_API_KEY` from environment)
