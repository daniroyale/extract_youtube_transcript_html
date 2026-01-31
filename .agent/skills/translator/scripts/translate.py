import argparse
import os
import re
from html.parser import HTMLParser
from typing import List, Tuple


# Language mapping for flexibility
LANGUAGE_MAP = {
    'pt': 'Portuguese',
    'portuguese': 'Portuguese',
    'portugues': 'Portuguese',
    'português': 'Portuguese',
    'es': 'Spanish',
    'spanish': 'Spanish',
    'español': 'Spanish',
    'espanol': 'Spanish',
    'en': 'English',
    'english': 'English',
    'ingles': 'English',
    'inglés': 'English'
}

# Short codes for file naming
LANGUAGE_CODES = {
    'Portuguese': 'pt',
    'Spanish': 'es',
    'English': 'en'
}


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML while preserving structure."""
    
    def __init__(self):
        super().__init__()
        self.text_segments = []
        self.current_pos = 0
        
    def handle_data(self, data):
        """Capture text data with its position."""
        if data.strip():  # Only capture non-empty text
            self.text_segments.append({
                'text': data,
                'start': self.current_pos,
                'end': self.current_pos + len(data)
            })
        self.current_pos += len(data)
    
    def handle_starttag(self, tag, attrs):
        """Track position through tags."""
        # Approximate tag length
        tag_str = f"<{tag}"
        for attr, value in attrs:
            tag_str += f' {attr}="{value}"' if value else f' {attr}'
        tag_str += ">"
        self.current_pos += len(tag_str)
    
    def handle_endtag(self, tag):
        """Track position through closing tags."""
        self.current_pos += len(f"</{tag}>")
    
    def handle_startendtag(self, tag, attrs):
        """Track self-closing tags."""
        tag_str = f"<{tag}"
        for attr, value in attrs:
            tag_str += f' {attr}="{value}"' if value else f' {attr}'
        tag_str += "/>"
        self.current_pos += len(tag_str)


def detect_format(content: str) -> str:
    """Detect if content is HTML or plain text."""
    # Simple heuristic: if it contains HTML tags, treat as HTML
    html_pattern = re.compile(r'<[^>]+>')
    if html_pattern.search(content):
        return 'html'
    return 'text'


def extract_text_from_html(html_content: str) -> List[Tuple[str, int, int]]:
    """
    Extract text segments from HTML with their positions.
    Returns list of (text, start_pos, end_pos) tuples.
    """
    # Use regex to find text between tags more reliably
    text_segments = []
    
    # Pattern to match text content (not inside tags)
    # This captures text that's not part of HTML tags
    pattern = re.compile(r'>([^<]+)<')
    
    for match in pattern.finditer(html_content):
        text = match.group(1).strip()
        if text:  # Only include non-empty text
            text_segments.append((text, match.start(1), match.end(1)))
    
    return text_segments


def chunk_text(text: str, max_chunk_size: int = 4000) -> List[str]:
    """
    Split text into chunks for translation.
    Tries to split at sentence boundaries.
    """
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by sentences (simple approach)
    sentences = re.split(r'([.!?]\s+)', text)
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        separator = sentences[i + 1] if i + 1 < len(sentences) else ""
        
        if len(current_chunk) + len(sentence) + len(separator) <= max_chunk_size:
            current_chunk += sentence + separator
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence + separator
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def translate_text(text: str, target_language: str, chunk_size: int = 4000) -> str:
    """
    Translate text to target language.
    This is a placeholder that prints instructions for the agent.
    """
    chunks = chunk_text(text, chunk_size)
    translated_chunks = []
    
    print(f"\n{'='*60}")
    print(f"TRANSLATION REQUIRED - {len(chunks)} chunk(s) to translate")
    print(f"Target Language: {target_language}")
    print(f"{'='*60}\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- CHUNK {i}/{len(chunks)} ---")
        print(f"Original text:\n{chunk}\n")
        print(f"AGENT: Please translate the above text to {target_language}.")
        print(f"Maintain the original tone, style, and meaning.")
        print(f"Provide ONLY the translated text, no explanations.")
        print(f"\nEnter translation (or press Enter to use placeholder):")
        
        # For automated processing, this would be replaced by actual AI translation
        # For now, we'll use a placeholder
        translation = input().strip()
        
        if not translation:
            translation = f"[TRANSLATION TO {target_language.upper()} NEEDED: {chunk[:50]}...]"
        
        translated_chunks.append(translation)
        print(f"✓ Chunk {i} translated\n")
    
    return " ".join(translated_chunks)


def translate_html(html_content: str, target_language: str, chunk_size: int = 4000) -> str:
    """
    Translate HTML content while preserving structure.
    """
    # Extract text segments with positions
    text_segments = extract_text_from_html(html_content)
    
    if not text_segments:
        print("No translatable text found in HTML.")
        return html_content
    
    # Collect all text to translate
    all_text = " [SEP] ".join([seg[0] for seg in text_segments])
    
    # Translate the combined text
    translated_text = translate_text(all_text, target_language, chunk_size)
    
    # Split translated text back into segments
    translated_segments = translated_text.split(" [SEP] ")
    
    # Ensure we have the same number of segments
    if len(translated_segments) != len(text_segments):
        print(f"Warning: Segment count mismatch. Original: {len(text_segments)}, Translated: {len(translated_segments)}")
        # Pad or truncate as needed
        while len(translated_segments) < len(text_segments):
            translated_segments.append("[TRANSLATION ERROR]")
        translated_segments = translated_segments[:len(text_segments)]
    
    # Reconstruct HTML with translated text
    result = html_content
    offset = 0
    
    for i, (original_text, start, end) in enumerate(text_segments):
        translated = translated_segments[i].strip()
        
        # Adjust positions based on previous replacements
        adjusted_start = start + offset
        adjusted_end = end + offset
        
        # Replace the text
        result = result[:adjusted_start] + translated + result[adjusted_end:]
        
        # Update offset for next replacement
        offset += len(translated) - len(original_text)
    
    return result


def translate_plain_text(text_content: str, target_language: str, chunk_size: int = 4000) -> str:
    """
    Translate plain text content.
    """
    return translate_text(text_content, target_language, chunk_size)


def translate_file(input_file: str, output_file: str, target_language: str, 
                   chunk_size: int = 4000, force_format: str = 'auto'):
    """
    Main function to translate a file.
    """
    # Validate language
    lang_key = target_language.lower()
    if lang_key not in LANGUAGE_MAP:
        print(f"Error: Unsupported language '{target_language}'")
        print(f"Supported languages: {', '.join(set(LANGUAGE_MAP.values()))}")
        return
    
    full_language = LANGUAGE_MAP[lang_key]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Detect format
    if force_format == 'auto':
        file_format = detect_format(content)
    else:
        file_format = force_format
    
    print(f"Input file: {input_file}")
    print(f"Detected format: {file_format.upper()}")
    print(f"Target language: {full_language}")
    print(f"Output file: {output_file}")
    
    # Translate based on format
    if file_format == 'html':
        translated_content = translate_html(content, full_language, chunk_size)
    else:
        translated_content = translate_plain_text(content, full_language, chunk_size)
    
    # Save output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        print(f"\n✓ Translation completed successfully!")
        print(f"✓ Saved to: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Translate documents while preserving format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate HTML to Spanish
  python translate.py article.html --lang es --out article_es.html
  
  # Translate text to Portuguese
  python translate.py transcript.txt --lang pt
  
  # Translate to English with custom chunk size
  python translate.py document.html --lang en --chunk-size 3000
  
Supported languages:
  Portuguese: pt, portuguese, portugues
  Spanish: es, spanish, español, espanol
  English: en, english, ingles
        """
    )
    
    parser.add_argument("input_file", help="Path to the input file to translate")
    parser.add_argument("--lang", "-l", required=True, help="Target language (pt/es/en)")
    parser.add_argument("--out", "-o", help="Output file path (default: <input>_<lang>.<ext>)")
    parser.add_argument("--chunk-size", type=int, default=4000, 
                        help="Maximum characters per translation chunk (default: 4000)")
    parser.add_argument("--format", choices=['auto', 'html', 'text'], default='auto',
                        help="Force format detection (default: auto)")
    
    args = parser.parse_args()
    
    # Generate output filename if not provided
    if not args.out:
        base, ext = os.path.splitext(args.input_file)
        lang_key = args.lang.lower()
        lang_code = LANGUAGE_CODES.get(LANGUAGE_MAP.get(lang_key, 'en'), 'en')
        args.out = f"{base}_{lang_code}{ext}"
    
    translate_file(
        args.input_file,
        args.out,
        args.lang,
        args.chunk_size,
        args.format
    )
