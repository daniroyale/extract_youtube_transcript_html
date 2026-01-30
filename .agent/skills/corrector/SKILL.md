---
name: grammar_corrector
description: Splits a text file into manageable chunks and prompts for grammar and punctuation correction.
---

# Grammar and Punctuation Corrector

This skill assists in processing large text files to correct grammar and add missing punctuation. It works by splitting the file into smaller chunks that can be processed effectively.

## Usage

### 1. Split the Text

First, run the Python script to split your large text file into smaller chunks (default ~7500 chars) to maintain narrative coherence.

```bash
python .agent/skills/corrector/scripts/chunk_text.py <INPUT_FILE>
```

**Options:**
- `input_file`: Path to the text file.
- `--size`: Chunk size (default 7500).
- `--out`: Custom output directory.

### 2. Process Chunks (Agent Instructions)

After splitting the text, the Agent should:

1.  **Iterate** through each generated chunk file in the output directory.
2.  **Rewrite** the content of each chunk. The goal is to:
    -   Correct grammatical errors.
    -   Add missing punctuation (periods, commas, question marks).
    -   Fix capitalization.
    -   Ensure proper paragraph breaks for readability.
    -   Maintain the original narrative flow and tone.
    -   Maintain the original language.
3.  **Output** the corrected text. This can be done by overwriting the chunk or creating a new `processed_chunk_X.txt` file.
