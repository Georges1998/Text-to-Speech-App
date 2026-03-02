# Text-to-Speech App

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![CLI](https://img.shields.io/badge/interface-CLI-informational)

A Python CLI that converts text into spoken audio using OpenAI's TTS API and merges audio files.

## Setup

### 1. Clone and navigate to the project

```bash
git clone https://github.com/YOUR_USERNAME/tts-app.git
cd tts-app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API key

Copy the example env file and add your key:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder with your actual key:

```bash
OPENAI_API_KEY=sk-your-key-here
```

## Usage

The CLI has two subcommands: `voice` and `merge`.

### `voice` - Convert text to speech

```bash
python3 tts.py voice input.txt
```

This reads `input.txt` and generates an MP3 file in `./output/` using the defaults from `config.yaml`.

#### Choose a voice and model

```bash
python3 tts.py voice input.txt --voice marin --model gpt-4o-mini-tts
```

#### Add style instructions

Control tone, accent, emotion, speed, and more (works with `gpt-4o-mini-tts` only):

```bash
python3 tts.py voice script.txt -i "Speak with a warm, friendly tone like telling a story"
python3 tts.py voice news.txt -i "Speak urgently like a news anchor"
```

#### Specify output file or format

```bash
python3 tts.py voice input.txt -o greeting.mp3
python3 tts.py voice input.txt --format wav
python3 tts.py voice input.txt --output-dir ./audio
```

#### All voice options

```text
python3 tts.py voice <file> [OPTIONS]

Arguments:
  file                        Path to the text file

Options:
  --voice, -v VOICE           Voice to use (default: from config)
  --model, -m MODEL           TTS model (default: from config)
  --format, -f FORMAT         Output audio format (default: mp3)
  --output, -o PATH           Output file path
  --output-dir DIR            Output directory (default: ./output)
  --instructions, -i TEXT     Voice style instructions (gpt-4o-mini-tts only)
```

### `merge` - Merge audio files

Combine all audio files in a folder into a single file, sorted alphabetically:

```bash
python3 tts.py merge ./output
```

This merges all `.mp3` files in `./output/` into `./output/merged.mp3`.

#### Custom output and format

```bash
python3 tts.py merge ./output -o final.mp3
python3 tts.py merge ./audio -f wav
```

#### All merge options

```text
python3 tts.py merge <folder> [OPTIONS]

Arguments:
  folder                      Folder containing audio files to merge

Options:
  --output, -o PATH           Output file path (default: <folder>/merged.<format>)
  --format, -f FORMAT         Audio file extension to merge (default: mp3)
```

## Configuration

Edit `config.yaml` to change defaults so you do not have to pass flags every time:

```yaml
model: gpt-4o-mini-tts
voice: coral
output_format: mp3
output_dir: ./output
instructions: "Speak clearly and naturally."
```

CLI flags always override config values.

## Available Options

### Models

| Model | Notes |
|---|---|
| `gpt-4o-mini-tts` | Latest, supports style instructions |
| `tts-1` | Lower latency, lower quality |
| `tts-1-hd` | Higher quality, higher latency |

### Voices

| Voice | Available on |
|---|---|
| `alloy`, `ash`, `coral`, `echo`, `fable`, `nova`, `onyx`, `sage`, `shimmer` | All models |
| `ballad`, `verse`, `marin`, `cedar` | `gpt-4o-mini-tts` only |

Best quality: **marin** and **cedar**.

### Output Formats

| Format | Best for |
|---|---|
| `mp3` | General use (default) |
| `wav` | Low-latency apps, no decoding overhead |
| `opus` | Streaming, low latency |
| `aac` | YouTube, Android, iOS |
| `flac` | Lossless archiving |
| `pcm` | Raw audio (24kHz, 16-bit signed, little-endian) |

### Supported Languages

The model supports 50+ languages. Put your target-language text in a file, then run:

```bash
python3 tts.py voice french.txt -i "Speak in French with a Parisian accent"
python3 tts.py voice spanish.txt -i "Speak in Spanish"
```

## Contributing

Contributions are welcome. See `CONTRIBUTING.md` for development setup and pull request guidelines.

## License

This project is licensed under the MIT License. See `LICENSE`.
