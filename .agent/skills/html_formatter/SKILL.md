---
name: html_formatter
description: Converts plain text files into HTML fragments compatible with WordPress Custom HTML blocks.
---

# HTML Formatter for WordPress

This skill converts plain text files into beautifully styled HTML suitable for pasting directly into a WordPress "Custom HTML" block or code editor. It handles paragraph wrapping, heading detection, and applies professional CSS styling.

## Features

✨ **Professional CSS Styling**: Inline CSS styles for modern typography and readability
📦 **Wrapper Container**: Optional div wrapper with scoped styles
🎨 **Customizable**: Control styles, wrapper, and CSS class names
🔒 **WordPress Compatible**: Works perfectly with WordPress Custom HTML blocks
🛡️ **Safe**: HTML special characters are properly escaped

## Usage

### 1. Basic Usage (with styles)

Run the Python script to convert your text file with default styling:

```bash
python .agent/skills/html_formatter/scripts/format_html.py <INPUT_FILE> --out <OUTPUT_FILE>
```

### 2. Command-Line Options

**Required:**
- `input_file`: Path to the source text file.

**Optional:**
- `--out`, `-o`: Path to save the generated HTML file. If omitted, prints to console.
- `--no-styles`: Disable inline CSS styles (generates plain HTML).
- `--no-wrapper`: Don't wrap content in a container div.
- `--class <NAME>`: Custom CSS class name for wrapper div (default: `formatted-content`).

### 3. Usage Examples

**Default (with styles and wrapper):**
```bash
python .agent/skills/html_formatter/scripts/format_html.py input.txt -o output.html
```

**Plain HTML without styles:**
```bash
python .agent/skills/html_formatter/scripts/format_html.py input.txt -o output.html --no-styles
```

**With custom CSS class:**
```bash
python .agent/skills/html_formatter/scripts/format_html.py input.txt -o output.html --class my-article
```

**Without wrapper div:**
```bash
python .agent/skills/html_formatter/scripts/format_html.py input.txt -o output.html --no-wrapper
```

### 4. Formatting Rules Applied

- **Paragraphs**: Blocks of text separated by double newlines (`\n\n`) are wrapped in `<p>` tags with professional styling.
- **Headings**: Lines starting with `#` are converted to headings (e.g., `# Title` -> `<h1>`, `## Subtitle` -> `<h2>`).
- **CSS Styles**: Inline styles include modern typography, proper spacing, and visual hierarchy.
- **Safety**: Special characters (`<`, `>`, `&`) are escaped to prevent broken HTML.

### 5. CSS Styling Details

The default styles include:

- **Typography**: Modern font stack (Inter, Segoe UI, Roboto)
- **Readability**: Optimized line height (1.8) and font sizes
- **Hierarchy**: Progressive heading sizes with proper margins
- **Visual Polish**: H2 headings include subtle bottom borders
- **Container**: Max-width 800px, centered with padding

## Example

### Input (`draft.txt`):
```text
# My Article Title

This is the first paragraph with important content.

## Section 1

Here is another paragraph with more details.

### Subsection

Additional information here.
```

### Command:
```bash
python .agent/skills/html_formatter/scripts/format_html.py draft.txt -o article.html
```

### Output (`article.html`):
```html
<div class="formatted-content" style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif; line-height: 1.8; color: #333">
<h1 style="font-size: 2.5em; font-weight: 700; margin: 1.5em 0 0.5em 0; color: #1a1a1a; line-height: 1.2">My Article Title</h1>
<p style="margin: 1em 0; font-size: 1.1em; text-align: justify">This is the first paragraph with important content.</p>
<h2 style="font-size: 2em; font-weight: 600; margin: 1.3em 0 0.5em 0; color: #2a2a2a; line-height: 1.3; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.3em">Section 1</h2>
<p style="margin: 1em 0; font-size: 1.1em; text-align: justify">Here is another paragraph with more details.</p>
<h3 style="font-size: 1.5em; font-weight: 600; margin: 1.2em 0 0.5em 0; color: #3a3a3a">Subsection</h3>
<p style="margin: 1em 0; font-size: 1.1em; text-align: justify">Additional information here.</p>
</div>
```

## WordPress Integration

Simply copy the generated HTML and paste it into a **Custom HTML** block in WordPress. The inline styles ensure your content looks professional without conflicting with your theme's CSS.
