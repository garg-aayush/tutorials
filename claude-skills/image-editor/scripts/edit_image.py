#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow>=10.0.0",
#     "pillow-heif>=0.13.0",
# ]
# ///
"""
Image editing script supporting format conversion, basic edits, and color adjustments.
Supports JPEG, PNG, TIFF, HEIC, and WebP formats.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageEnhance
import pillow_heif

# Register HEIF opener
pillow_heif.register_heif_opener()


def load_image(input_path):
    """Load an image from the given path."""
    try:
        img = Image.open(input_path)
        return img
    except Exception as e:
        print(f"Error loading image: {e}", file=sys.stderr)
        sys.exit(1)


def save_image(img, output_path, format_override=None):
    """Save an image to the given path with optional format override."""
    try:
        # Determine format from output path or override
        if format_override:
            save_format = format_override.upper()
        else:
            save_format = Path(output_path).suffix[1:].upper()
        
        # Handle format aliases
        if save_format == 'JPG':
            save_format = 'JPEG'
        
        # Convert RGBA to RGB for formats that don't support transparency
        if save_format in ['JPEG', 'BMP'] and img.mode in ['RGBA', 'LA', 'P']:
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ['RGBA', 'LA'] else None)
            img = background
        
        img.save(output_path, format=save_format)
        print(f"Image saved to: {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}", file=sys.stderr)
        sys.exit(1)


def convert_format(img, target_format):
    """Convert image to target format."""
    # Format conversion is handled in save_image
    return img


def rotate_image(img, degrees):
    """Rotate image by specified degrees (90, 180, 270, or any angle)."""
    try:
        # Expand=True maintains full image content for non-90 degree rotations
        return img.rotate(-degrees, expand=True)
    except Exception as e:
        print(f"Error rotating image: {e}", file=sys.stderr)
        sys.exit(1)


def resize_image(img, width=None, height=None, keep_aspect=True):
    """Resize image with optional aspect ratio preservation."""
    try:
        if width is None and height is None:
            return img
        
        original_width, original_height = img.size
        
        if keep_aspect:
            if width and height:
                # Calculate which dimension to constrain
                width_ratio = width / original_width
                height_ratio = height / original_height
                ratio = min(width_ratio, height_ratio)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
            elif width:
                ratio = width / original_width
                new_width = width
                new_height = int(original_height * ratio)
            else:  # height only
                ratio = height / original_height
                new_height = height
                new_width = int(original_width * ratio)
        else:
            new_width = width or original_width
            new_height = height or original_height
        
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Error resizing image: {e}", file=sys.stderr)
        sys.exit(1)


def adjust_brightness(img, factor):
    """Adjust image brightness. Factor > 1.0 brightens, < 1.0 darkens."""
    try:
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)
    except Exception as e:
        print(f"Error adjusting brightness: {e}", file=sys.stderr)
        sys.exit(1)


def adjust_contrast(img, factor):
    """Adjust image contrast. Factor > 1.0 increases, < 1.0 decreases."""
    try:
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor)
    except Exception as e:
        print(f"Error adjusting contrast: {e}", file=sys.stderr)
        sys.exit(1)


def adjust_saturation(img, factor):
    """Adjust image saturation. Factor > 1.0 increases, < 1.0 decreases."""
    try:
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(factor)
    except Exception as e:
        print(f"Error adjusting saturation: {e}", file=sys.stderr)
        sys.exit(1)


def replace_transparency(img, color=(255, 255, 255)):
    """Replace transparency with a solid color (default: white)."""
    try:
        if img.mode not in ['RGBA', 'LA', 'P']:
            print("Image has no transparency channel", file=sys.stderr)
            return img
        
        # Convert palette images to RGBA first
        if img.mode == 'P':
            img = img.convert('RGBA')
        
        # Create background with specified color
        background = Image.new('RGB', img.size, color)
        
        # Paste image onto background using alpha channel as mask
        if img.mode in ['RGBA', 'LA']:
            background.paste(img, mask=img.split()[-1])
        
        return background
    except Exception as e:
        print(f"Error replacing transparency: {e}", file=sys.stderr)
        sys.exit(1)


def flip_image(img, direction):
    """Flip image horizontally or vertically."""
    try:
        if direction == 'horizontal':
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            print(f"Invalid flip direction: {direction}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error flipping image: {e}", file=sys.stderr)
        sys.exit(1)


def parse_color(color_str):
    """Parse color string in format 'R,G,B' to tuple."""
    try:
        r, g, b = map(int, color_str.split(','))
        return (r, g, b)
    except:
        print(f"Invalid color format: {color_str}. Use format 'R,G,B' (e.g., '255,255,255')", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Image editing tool supporting format conversion, basic edits, and color adjustments.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert JPEG to PNG
  python edit_image.py input.jpg output.png

  # Rotate 90 degrees and increase brightness by 20%
  python edit_image.py input.jpg output.jpg --rotate 90 --brightness 1.2

  # Resize keeping aspect ratio
  python edit_image.py input.jpg output.jpg --width 800 --height 600 --keep-aspect

  # Replace transparency with white
  python edit_image.py input.png output.png --replace-transparency 255,255,255

  # Chain multiple operations
  python edit_image.py input.jpg output.png --rotate 90 --brightness 1.2 --saturation 1.1
        """
    )
    
    parser.add_argument('input', help='Input image path')
    parser.add_argument('output', help='Output image path')
    
    # Format conversion
    parser.add_argument('--format', help='Target format (JPEG, PNG, TIFF, HEIC, WEBP)')
    
    # Basic edits
    parser.add_argument('--rotate', type=float, help='Rotation angle in degrees (e.g., 90, 180, 270)')
    parser.add_argument('--width', type=int, help='Target width in pixels')
    parser.add_argument('--height', type=int, help='Target height in pixels')
    parser.add_argument('--keep-aspect', action='store_true', help='Maintain aspect ratio when resizing')
    parser.add_argument('--flip', choices=['horizontal', 'vertical'], help='Flip direction')
    
    # Color adjustments
    parser.add_argument('--brightness', type=float, help='Brightness factor (>1.0 brightens, <1.0 darkens)')
    parser.add_argument('--contrast', type=float, help='Contrast factor (>1.0 increases, <1.0 decreases)')
    parser.add_argument('--saturation', type=float, help='Saturation factor (>1.0 increases, <1.0 decreases)')
    
    # Transparency handling
    parser.add_argument('--replace-transparency', type=str, help='Replace transparency with color (format: R,G,B, e.g., 255,255,255 for white)')
    
    args = parser.parse_args()
    
    # Load image
    img = load_image(args.input)
    
    # Apply operations in a logical order
    
    # 1. Transparency replacement (before color adjustments)
    if args.replace_transparency:
        color = parse_color(args.replace_transparency)
        img = replace_transparency(img, color)
    
    # 2. Geometric transformations
    if args.rotate is not None:
        img = rotate_image(img, args.rotate)
    
    if args.flip:
        img = flip_image(img, args.flip)
    
    if args.width or args.height:
        img = resize_image(img, args.width, args.height, args.keep_aspect)
    
    # 3. Color adjustments
    if args.brightness:
        img = adjust_brightness(img, args.brightness)
    
    if args.contrast:
        img = adjust_contrast(img, args.contrast)
    
    if args.saturation:
        img = adjust_saturation(img, args.saturation)
    
    # 4. Save with format conversion if needed
    save_image(img, args.output, args.format)


if __name__ == '__main__':
    main()
