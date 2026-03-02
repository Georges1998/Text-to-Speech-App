#!/usr/bin/env python3
"""Text-to-Speech CLI — generate speech and merge audio files."""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

VALID_MODELS = ["gpt-4o-mini-tts", "tts-1", "tts-1-hd"]
VALID_VOICES_FULL = [
    "alloy", "ash", "ballad", "coral", "echo", "fable",
    "nova", "onyx", "sage", "shimmer", "verse", "marin", "cedar",
]
VALID_VOICES_BASIC = [
    "alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer",
]
VALID_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]


def load_config(config_path: str = "config.yaml") -> dict:
    path = Path(config_path)
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f) or {}
    return {}


def validate_options(model: str, voice: str, output_format: str) -> None:
    if model not in VALID_MODELS:
        sys.exit(f"Error: Invalid model '{model}'. Choose from: {', '.join(VALID_MODELS)}")

    valid_voices = VALID_VOICES_FULL if model == "gpt-4o-mini-tts" else VALID_VOICES_BASIC
    if voice not in valid_voices:
        sys.exit(f"Error: Invalid voice '{voice}' for model '{model}'. Choose from: {', '.join(valid_voices)}")

    if output_format not in VALID_FORMATS:
        sys.exit(f"Error: Invalid format '{output_format}'. Choose from: {', '.join(VALID_FORMATS)}")


def generate_speech(
    text: str,
    model: str,
    voice: str,
    output_format: str,
    output_path: Path,
    instructions: Optional[str] = None,
) -> None:
    client = OpenAI()

    kwargs = {
        "model": model,
        "voice": voice,
        "input": text,
        "response_format": output_format,
    }
    if instructions and model == "gpt-4o-mini-tts":
        kwargs["instructions"] = instructions

    print(f"Generating speech...")
    print(f"  Model:   {model}")
    print(f"  Voice:   {voice}")
    print(f"  Format:  {output_format}")
    if instructions and model == "gpt-4o-mini-tts":
        print(f"  Style:   {instructions}")
    print(f"  Output:  {output_path}")

    with client.audio.speech.with_streaming_response.create(**kwargs) as response:
        response.stream_to_file(str(output_path))

    print(f"Done! Audio saved to {output_path}")


def cmd_voice(args: argparse.Namespace, config: dict) -> None:
    file_path = Path(args.file)
    if not file_path.exists():
        sys.exit(f"Error: File '{args.file}' not found.")

    text = file_path.read_text().strip()
    if not text:
        sys.exit("Error: Text file is empty.")

    model = args.model or config.get("model", "gpt-4o-mini-tts")
    voice = args.voice or config.get("voice", "coral")
    fmt = args.format or config.get("output_format", "mp3")
    instructions = args.instructions or config.get("instructions")

    validate_options(model, voice, fmt)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path(args.output_dir or config.get("output_dir", "./output"))
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"speech_{timestamp}.{fmt}"

    generate_speech(
        text=text,
        model=model,
        voice=voice,
        output_format=fmt,
        output_path=output_path,
        instructions=instructions,
    )


def cmd_merge(args: argparse.Namespace) -> None:
    folder = Path(args.folder)
    if not folder.is_dir():
        sys.exit(f"Error: '{args.folder}' is not a directory.")

    ext = args.format or "mp3"
    files = sorted(f for f in folder.iterdir() if f.suffix == f".{ext}" and f.name != os.path.basename(args.output or ""))

    if not files:
        sys.exit(f"Error: No .{ext} files found in '{folder}'.")

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = folder / f"merged.{ext}"

    print(f"Merging {len(files)} .{ext} files from {folder}:")
    with open(output_path, "wb") as out:
        for f in files:
            size = f.stat().st_size
            print(f"  + {f.name} ({size / 1024:.0f} KB)")
            with open(f, "rb") as inp:
                out.write(inp.read())

    total_size = output_path.stat().st_size
    print(f"\nSaved to {output_path} ({total_size / 1024 / 1024:.1f} MB)")


def main() -> None:
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Text-to-Speech CLI — generate speech and merge audio files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  python tts.py voice input.txt
  python tts.py voice input.txt --voice marin --model gpt-4o-mini-tts
  python tts.py voice input.txt -o output/greeting.mp3
  python tts.py voice input.txt -i "Speak with excitement"
  python tts.py merge ./output
  python tts.py merge ./output -o final.mp3
        """,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- voice subcommand ---
    voice_parser = subparsers.add_parser("voice", help="Convert a text file to speech")
    voice_parser.add_argument("file", help="Path to the text file")
    voice_parser.add_argument("--voice", "-v", default=None, help="Voice to use (default: from config)")
    voice_parser.add_argument("--model", "-m", default=None, help="TTS model (default: from config)")
    voice_parser.add_argument("--format", "-f", default=None, help="Output audio format (default: mp3)")
    voice_parser.add_argument("--output", "-o", default=None, help="Output file path")
    voice_parser.add_argument("--output-dir", default=None, help="Output directory (default: ./output)")
    voice_parser.add_argument("--instructions", "-i", default=None, help="Voice style instructions (gpt-4o-mini-tts only)")

    # --- merge subcommand ---
    merge_parser = subparsers.add_parser("merge", help="Merge audio files in a folder alphabetically")
    merge_parser.add_argument("folder", help="Folder containing audio files to merge")
    merge_parser.add_argument("--output", "-o", default=None, help="Output file path (default: <folder>/merged.<format>)")
    merge_parser.add_argument("--format", "-f", default=None, help="Audio file extension to merge (default: mp3)")

    args = parser.parse_args()

    if args.command == "voice":
        cmd_voice(args, config)
    elif args.command == "merge":
        cmd_merge(args)


if __name__ == "__main__":
    main()
