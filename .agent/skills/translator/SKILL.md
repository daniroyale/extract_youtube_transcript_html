---
name: translator
description: Translates documents to Portuguese, Spanish, or English while preserving the original format.
---

# Document Translator

This skill translates documents to different languages while preserving the original format. It supports HTML, plain text, and other formats, ensuring the translated output maintains the same structure as the input.

## Supported Languages

- **Portuguese** (`pt`, `portuguese`, `portugues`)
- **Spanish** (`es`, `spanish`, `español`, `espanol`)
- **English** (`en`, `english`, `ingles`)

## Features

✨ **Format Preservation**: Maintains the original document structure (HTML tags, formatting, etc.)
🌍 **Multiple Languages**: Supports Portuguese, Spanish, and English
🎯 **Smart Translation**: Translates only text content, preserving HTML tags and special characters
📦 **Chunked Processing**: Handles large documents by splitting into manageable chunks
🔒 **Safe**: Preserves HTML entities and special formatting

## Usage

### 1. Basic Translation

Translate a document to a target language:

```bash
python .agent/skills/translator/scripts/translate.py <INPUT_FILE> --lang <LANGUAGE> --out <OUTPUT_FILE>
```

### 2. Command-Line Options

**Required:**
- `input_file`: Path to the source file to translate.
- `--lang`, `-l`: Target language (pt/portuguese/portugues, es/spanish/español/espanol, en/english/ingles).

**Optional:**
- `--out`, `-o`: Path to save the translated file. If omitted, saves as `<input_file>_<lang>.<ext>`.
- `--chunk-size`: Maximum characters per translation chunk (default: 4000).
- `--format`: Force format detection (auto/html/text). Default is auto-detect.

### 3. Usage Examples

**Translate HTML to Spanish:**
```bash
python .agent/skills/translator/scripts/translate.py article.html --lang es --out article_es.html
```

**Translate text file to Portuguese:**
```bash
python .agent/skills/translator/scripts/translate.py transcript.txt --lang pt
```

**Translate to English with custom output:**
```bash
python .agent/skills/translator/scripts/translate.py document.html --lang en --out english_version.html
```

**Auto-detect format and translate:**
```bash
python .agent/skills/translator/scripts/translate.py content.txt --lang spanish --out contenido.txt
```

### 4. How It Works

1. **Format Detection**: Automatically detects if the input is HTML or plain text.
2. **Content Extraction**: For HTML files, extracts text while preserving tags and structure.
3. **Chunking**: Splits large content into manageable chunks to ensure quality translation.
4. **Translation**: Uses AI to translate each chunk while maintaining context.
5. **Reconstruction**: Reassembles the translated content in the original format.
6. **Output**: Saves the translated document with the same structure as the original.

### 5. Format Handling

**HTML Files:**
- Preserves all HTML tags (`<div>`, `<p>`, `<h1>`, etc.)
- Maintains inline styles and attributes
- Translates only text content between tags
- Keeps HTML entities intact

**Text Files:**
- Preserves paragraph breaks
- Maintains line structure
- Translates all text content

## Example

### Input (`article.html`):
```html
<div class="formatted-content" style="max-width: 800px">
<h1 style="font-size: 2.5em">My Article Title</h1>
<p style="margin: 1em 0">This is the first paragraph with important content.</p>
<h2 style="font-size: 2em">Section 1</h2>
<p style="margin: 1em 0">Here is another paragraph with more details.</p>
</div>
```

### Command:
```bash
python .agent/skills/translator/scripts/translate.py article.html --lang es --out article_es.html
```

### Output (`article_es.html`):
```html
<div class="formatted-content" style="max-width: 800px">
<h1 style="font-size: 2.5em">Mi Título de Artículo</h1>
<p style="margin: 1em 0">Este es el primer párrafo con contenido importante.</p>
<h2 style="font-size: 2em">Sección 1</h2>
<p style="margin: 1em 0">Aquí hay otro párrafo con más detalles.</p>
</div>
```

## Agent Instructions

When using this skill, the agent should:

1. **Verify Input**: Ensure the input file exists and is readable.
2. **Run Translation**: Execute the script with appropriate parameters.
3. **Validate Output**: Check that the output file was created successfully.
4. **Preserve Format**: Ensure the translated document maintains the original structure.
5. **Handle Errors**: Report any translation errors or format issues to the user.

## Notes

- The translation quality depends on the AI model's capabilities.
- Very large files may take longer to process due to chunking.
- HTML structure is preserved, but complex JavaScript or CSS may require manual review.
- The script uses context-aware translation to maintain coherence across chunks.
