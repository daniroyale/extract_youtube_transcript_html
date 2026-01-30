import argparse
import os
import html

# Default CSS styles for the content
DEFAULT_STYLES = {
    'wrapper': {
        'max-width': '800px',
        'margin': '0 auto',
        'padding': '20px',
        'font-family': "'Inter', 'Segoe UI', 'Roboto', sans-serif",
        'line-height': '1.8',
        'color': '#333'
    },
    'h1': {
        'font-size': '2.5em',
        'font-weight': '700',
        'margin': '1.5em 0 0.5em 0',
        'color': '#1a1a1a',
        'line-height': '1.2'
    },
    'h2': {
        'font-size': '2em',
        'font-weight': '600',
        'margin': '1.3em 0 0.5em 0',
        'color': '#2a2a2a',
        'line-height': '1.3',
        'border-bottom': '2px solid #e0e0e0',
        'padding-bottom': '0.3em'
    },
    'h3': {
        'font-size': '1.5em',
        'font-weight': '600',
        'margin': '1.2em 0 0.5em 0',
        'color': '#3a3a3a'
    },
    'h4': {
        'font-size': '1.25em',
        'font-weight': '600',
        'margin': '1em 0 0.5em 0',
        'color': '#4a4a4a'
    },
    'h5': {
        'font-size': '1.1em',
        'font-weight': '600',
        'margin': '1em 0 0.5em 0',
        'color': '#5a5a5a'
    },
    'h6': {
        'font-size': '1em',
        'font-weight': '600',
        'margin': '1em 0 0.5em 0',
        'color': '#6a6a6a'
    },
    'p': {
        'margin': '1em 0',
        'font-size': '1.1em',
        'text-align': 'justify'
    }
}

def dict_to_inline_style(style_dict):
    """Convert a dictionary of CSS properties to an inline style string."""
    return '; '.join([f"{key}: {value}" for key, value in style_dict.items()])

def format_to_html(input_file, output_file, use_styles=True, use_wrapper=True, custom_class='formatted-content'):
    """
    Reads a text file and converts it to HTML fragments suitable for WordPress.
    
    Args:
        input_file: Path to the input text file
        output_file: Path to save the HTML output (None to print to console)
        use_styles: Whether to include inline CSS styles
        use_wrapper: Whether to wrap content in a div container
        custom_class: CSS class name for the wrapper div
    
    Rules:
    - distinct blocks separated by double newlines become <p> tags.
    - lines starting with '#' become headings (Markdown style).
    - existing HTML special characters are escaped.
    - CSS styles are applied inline for WordPress compatibility.
    """
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize newlines
    content = content.replace('\r\n', '\n')
    
    # Split by double newlines to find paragraphs
    blocks = content.split('\n\n')
    
    html_output = []
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Check for headings (Markdown style)
        if block.startswith('#'):
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            
            # Limit to h6
            level = min(level, 6)
            text_content = block[level:].strip()
            escaped_text = html.escape(text_content)
            
            # Apply inline styles if enabled
            if use_styles:
                style_attr = f' style="{dict_to_inline_style(DEFAULT_STYLES[f"h{level}"])}"'
            else:
                style_attr = ''
            
            html_output.append(f"<h{level}{style_attr}>{escaped_text}</h{level}>")
            
        else:
            # Regular paragraph
            escaped_text = html.escape(block)
            
            # Apply inline styles if enabled
            if use_styles:
                style_attr = f' style="{dict_to_inline_style(DEFAULT_STYLES["p"])}"'
            else:
                style_attr = ''
            
            html_output.append(f"<p{style_attr}>{escaped_text}</p>")

    # Join all HTML elements
    content_html = "\n".join(html_output)
    
    # Wrap in container div if requested
    if use_wrapper:
        wrapper_style = dict_to_inline_style(DEFAULT_STYLES['wrapper']) if use_styles else ''
        style_attr = f' style="{wrapper_style}"' if wrapper_style else ''
        final_html = f'<div class="{custom_class}"{style_attr}>\n{content_html}\n</div>'
    else:
        final_html = content_html
    
    # Save or print output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Successfully converted {input_file} to {output_file}")
        print(f"Styles applied: {use_styles}, Wrapper used: {use_wrapper}")
    else:
        print(final_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert text file to WordPress-compatible HTML with CSS styling.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion with styles (default)
  python format_html.py input.txt -o output.html
  
  # Without inline styles (plain HTML)
  python format_html.py input.txt -o output.html --no-styles
  
  # Without wrapper div
  python format_html.py input.txt -o output.html --no-wrapper
  
  # Custom CSS class name
  python format_html.py input.txt -o output.html --class my-custom-content
        """
    )
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("--out", "-o", help="Path to the output HTML file (prints to console if omitted)")
    parser.add_argument("--no-styles", action="store_true", help="Disable inline CSS styles")
    parser.add_argument("--no-wrapper", action="store_true", help="Don't wrap content in a container div")
    parser.add_argument("--class", dest="css_class", default="formatted-content", 
                        help="CSS class name for wrapper div (default: formatted-content)")
    
    args = parser.parse_args()
    
    format_to_html(
        args.input_file, 
        args.out,
        use_styles=not args.no_styles,
        use_wrapper=not args.no_wrapper,
        custom_class=args.css_class
    )
