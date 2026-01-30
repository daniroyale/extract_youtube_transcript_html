---
name: youtube_transcript
description: Extracts text transcripts from YouTube videos using their URL or ID.
---

# YouTube Transcript Extractor

This skill provides tools to extract transcripts from YouTube videos.

## Prerequisites

Install the required Python packages:

```bash
pip install -r skills/transcript/requirements.txt
```

## Usage

### Command Line Interface

You can use the python script directly to fetch a transcript.

```bash
python skills/transcript/scripts/get_transcript.py <YOUTUBE_URL>
```

**Options:**

- `url`: The YouTube URL or Video ID (required).
- `--lang`: Language code to fetch (default: 'en').
- `--output`, `-o`: Path to save the output text file. If not provided, prints to stdout.

### Examples

**Print to console:**
```bash
python skills/transcript/scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Save to file:**
```bash
python skills/transcript/scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o transcript.txt
```

**Specify language (e.g., Spanish):**
```bash
python skills/transcript/scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --lang es
```
