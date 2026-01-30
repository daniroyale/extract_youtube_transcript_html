import argparse
import os

def chunk_text(input_file, chunk_size=7500, output_dir=None):
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Create output directory based on input filename if not provided
    if not output_dir:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(os.path.dirname(input_file), f"{base_name}_chunks")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Splitting logic
    # We want chunks of approx chunk_size. 
    # look for the last space/newline before the limit.
    
    current_pos = 0
    total_len = len(text)
    part_num = 1
    
    while current_pos < total_len:
        end_pos = min(current_pos + chunk_size, total_len)
        
        # If we are not at the end of the text, try to find a safe break point
        if end_pos < total_len:
            # Look for last newline in the last 10% of the chunk to prioritize paragraphs
            search_window = int(chunk_size * 0.1)
            search_start = max(current_pos, end_pos - search_window)
            chunk_slice = text[search_start:end_pos]
            
            last_newline = chunk_slice.rfind('\n')
            if last_newline != -1:
                 end_pos = search_start + last_newline + 1 # Include the newline
            else:
                # No newline, look for last space to avoid splitting words
                last_space = chunk_slice.rfind(' ')
                if last_space != -1:
                    end_pos = search_start + last_space + 1
        
        chunk = text[current_pos:end_pos]
        
        output_filename = os.path.join(output_dir, f"chunk_{part_num:03d}.txt")
        with open(output_filename, 'w', encoding='utf-8') as out:
            out.write(chunk)
        
        print(f"Created {output_filename} ({len(chunk)} chars)")
        
        current_pos = end_pos
        part_num += 1

    print(f"\nSuccessfully split into {part_num-1} chunks in '{output_dir}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split text into chunks.")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("--size", type=int, default=7500, help="Approximate chunk size")
    parser.add_argument("--out", help="Output directory")
    
    args = parser.parse_args()
    chunk_text(args.input_file, args.size, args.out)
