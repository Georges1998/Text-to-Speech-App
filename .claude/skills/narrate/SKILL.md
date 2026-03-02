---
name: narrate
description: Transform a script into natural, human-like narration and generate speech using the TTS app. Use when the user wants to convert a script or text into expressive spoken audio with pauses, gasps, sighs, and other dramatic effects.
argument-hint: [script text or path to script file]
disable-model-invocation: true
---

# Narrate

Transform a script into expressive, human-like narration and run it through the TTS app.

## Input

`$ARGUMENTS` is either:
- Inline script text, OR
- A path to a text file containing the script

If it looks like a file path, read the file first.

## Transformation rules

Rewrite the script to sound like a skilled human narrator by applying these techniques:

### Inline effects (embed directly in the text)

- **Pauses**: Use `...` (ellipsis) for short pauses, `—` (em dash) for dramatic pauses, or `[pause]` for deliberate beats
- **Gasps**: Write `*gasp*` or the word "gasp" naturally where surprise occurs
- **Sighs**: Write `*sigh*` or weave "sigh" into the text naturally
- **Laughter**: Write `*chuckle*`, `ha`, or `heh` where appropriate
- **Hesitation**: Use `um`, `uh`, `well...` for natural hesitation
- **Emphasis**: Use CAPS sparingly for strong emphasis on key words
- **Breathing**: Add commas and sentence breaks where a narrator would naturally breathe

### Pacing

- Break long sentences into shorter ones for natural rhythm
- Add paragraph breaks between distinct thoughts or scene changes
- Use punctuation to control flow: commas slow down, short sentences speed up

### What NOT to do

- Don't add effects where they'd feel forced or unnatural
- Don't overload with effects — subtlety sounds more human
- Don't change the meaning or content of the script
- Don't add narration or commentary that wasn't in the original

## Output

After transforming the script:

1. **Show the transformed text** to the user so they can review it
2. **Craft an `--instructions` flag** tailored to the script's tone and content. Examples:
   - `"Narrate warmly and conversationally, with natural pauses and emotional inflection. Vary your pacing — slow down for dramatic moments, speed up for excitement."`
   - `"Read like an audiobook narrator. Use a calm, measured pace with slight dramatic flair. Let emotions come through naturally."`
   - `"Deliver with energy and enthusiasm, like a storyteller captivating an audience. Use vocal variety — whisper for suspense, project for emphasis."`
3. **Build and run the command**:

```bash
python3 tts.py "<transformed text>" --model gpt-4o-mini-tts --voice <voice> --instructions "<instructions>"
```

- Default voice: `coral` (or use the user's preference if stated)
- If the text is very long, use `--file` with a temp file instead of inline text
- Always use `gpt-4o-mini-tts` since it's the only model that supports instructions

4. **Report the output file path** when done.
