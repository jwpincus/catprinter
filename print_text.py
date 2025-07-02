#!/usr/bin/env python3
"""
Script to convert text files to images and print them on the cat thermal printer.
"""
import argparse
import os
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont

def convert_text_to_image(text_file, output_image, font_size=16, width=384):
    """Convert a text file to an image using PIL for better text control."""
    try:
        # Read the text file
        with open(text_file, 'r') as f:
            text_content = f.read().strip()
        
        if not text_content:
            print("Error: Text file is empty")
            return False
        
        # Try to load a system font with emoji support, fall back to default if not available
        try:
            # Try fonts with emoji support first, then regular fonts
            font_paths = [
                '/System/Library/Fonts/Apple Color Emoji.ttc',  # macOS emoji font
                '/System/Library/Fonts/Helvetica.ttc',  # macOS
                '/System/Library/Fonts/Arial.ttf',  # macOS
                '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',  # Linux emoji
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # Linux
                'C:\\Windows\\Fonts\\seguiemj.ttf',  # Windows emoji
                'C:\\Windows\\Fonts\\arial.ttf',  # Windows
            ]
            
            font = None
            emoji_font = None
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        test_font = ImageFont.truetype(font_path, font_size)
                        if 'emoji' in font_path.lower() or 'color' in font_path.lower():
                            emoji_font = test_font
                            print(f"Found emoji font: {font_path}")
                        else:
                            if font is None:  # Use first regular font found
                                font = test_font
                                print(f"Using font: {font_path}")
                    except Exception as e:
                        continue
            
            # Prefer emoji font if available, otherwise use regular font
            if emoji_font:
                font = emoji_font
            elif font is None:
                # Fall back to default font
                font = ImageFont.load_default()
                print(f"Warning: Using default font, no system fonts found")
        
        except Exception as e:
            font = ImageFont.load_default()
            print(f"Warning: Could not load custom font ({e}), using default")
        
        # Create a temporary image to measure text size
        temp_img = Image.new('RGB', (1, 1), color='white')
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Function to wrap text to fit within printer width
        def wrap_text_to_width(text, font, max_width):
            words = text.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                # Test if adding this word would exceed the width
                test_line = ' '.join(current_line + [word])
                bbox = temp_draw.textbbox((0, 0), test_line, font=font)
                line_width = bbox[2] - bbox[0]
                
                if line_width <= max_width or not current_line:  # Always add at least one word
                    current_line.append(word)
                else:
                    # Start new line
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            # Add the last line
            if current_line:
                lines.append(' '.join(current_line))
            
            return lines
        
        # Process all text with wrapping
        original_lines = text_content.split('\n')
        wrapped_lines = []
        available_width = width - 20  # Account for padding
        
        for original_line in original_lines:
            if original_line.strip():
                # Wrap long lines to fit printer width
                wrapped = wrap_text_to_width(original_line, font, available_width)
                wrapped_lines.extend(wrapped)
            else:
                # Preserve empty lines
                wrapped_lines.append('')
        
        # Measure wrapped lines
        line_heights = []
        for line in wrapped_lines:
            if line.strip():
                bbox = temp_draw.textbbox((0, 0), line, font=font)
                line_height = bbox[3] - bbox[1]
            else:
                line_height = font_size  # Use font size for empty lines
            line_heights.append(line_height)
        
        # Calculate image dimensions - now height grows with font size and wrapping
        total_height = sum(line_heights) + (len(wrapped_lines) - 1) * 5  # 5px line spacing
        img_width = width  # Use full printer width
        img_height = max(total_height + 20, 50)  # Add padding, min 50px
        
        # Create the actual image
        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw text line by line
        y_position = 10  # Top padding
        for i, line in enumerate(wrapped_lines):
            if line.strip():  # Only draw non-empty lines
                draw.text((10, y_position), line, fill='black', font=font)
            y_position += line_heights[i] + 5  # Move to next line with spacing
        
        # Save the image
        img.save(output_image, 'PNG')
        print(f"Created image: {img_width}x{img_height} pixels")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert text file to image and print on cat thermal printer')
    parser.add_argument('text_file', help='Text file to print')
    parser.add_argument('-s', '--font-size', type=int, default=16, help='Font size (default: 16)')
    parser.add_argument('-p', '--preview', action='store_true', help='Show preview before printing')
    parser.add_argument('-k', '--keep-image', action='store_true', help='Keep the generated image file')
    parser.add_argument('-o', '--output', help='Output image filename (default: temp file)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.text_file):
        print(f"Error: File '{args.text_file}' not found")
        sys.exit(1)
    
    # Determine output image filename
    if args.output:
        output_image = args.output
        temp_file = False
    else:
        # Create a temporary file
        temp_fd, output_image = tempfile.mkstemp(suffix='.png')
        os.close(temp_fd)
        temp_file = True
    
    try:
        # Convert text to image
        print(f"Converting '{args.text_file}' to image...")
        if not convert_text_to_image(args.text_file, output_image, args.font_size):
            sys.exit(1)
        
        print(f"Image created: {output_image}")
        
        # Build print command
        print_cmd = ['./print.py', output_image, ]
        if args.preview:
            print_cmd.append('-s')
        
        # Print the image
        print("Printing...")
        result = subprocess.run(print_cmd)
        
        if result.returncode == 0:
            print("✅ Print job completed successfully!")
        else:
            print("❌ Print job failed")
            
    finally:
        # Clean up temporary file if needed
        if temp_file and not args.keep_image and os.path.exists(output_image):
            os.unlink(output_image)
            print(f"Cleaned up temporary file: {output_image}")

if __name__ == '__main__':
    main()
