# Catprinter Python Package

A command-line utility for printing text and images on cat thermal printers via Bluetooth.

## Installation

Install in development mode (recommended for local development):
```bash
pip install -e .
```

Or install normally:
```bash
pip install .
```

## Usage

After installation, you'll have these commands available system-wide:

### Print Text Files
```bash
catprint-text myfile.txt
catprint-text myfile.txt -s 24 -p  # larger font with preview
```

### Print Images
```bash
catprint-image photo.jpg
catprint-image photo.jpg -s  # show preview
catprint myimage.png  # alias for catprint-image
```

## Commands

- `catprint-text` - Convert text files to images and print them
- `catprint-image` - Print image files directly  
- `catprint` - Alias for `catprint-image`

## Options

### Text Printing (`catprint-text`)
- `-s, --font-size` - Font size (default: 16)
- `-p, --preview` - Show preview before printing
- `-k, --keep-image` - Keep the generated image file
- `-o, --output` - Save image to specific file
- `-d, --device` - Specify printer device

### Image Printing (`catprint-image`, `catprint`)
- `-s, --show-preview` - Show preview before printing
- `-b, --img-binarization-algo` - Dithering algorithm
- `-d, --device` - Specify printer device
- `-e, --energy` - Thermal energy level
- `-l, --log-level` - Logging level

## Examples

```bash
# Print a text file with large font
catprint-text note.txt -s 28 -p

# Print an image with preview
catprint photo.jpg -s

# Print text and keep the generated image
catprint-text todo.txt -k -o todo-image.png
```
