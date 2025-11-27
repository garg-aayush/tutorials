---
name: image-editor
description: Image editing tool supporting format conversion (JPEG, PNG, TIFF, HEIC, WebP), basic edits (rotate, resize, flip), color adjustments (brightness, contrast, saturation), and transparency handling. Use when users request image editing tasks like "convert this JPEG to PNG", "rotate this image 90 degrees", "resize to 800x600 keeping aspect ratio", "increase brightness by 20%", or "replace transparency with white".
---

# Image Editor

This skill provides comprehensive image editing capabilities through a Python script that handles format conversions, basic edits, color adjustments, and transparency operations.

## Requirements

This skill uses [uv](https://docs.astral.sh/uv/) for dependency management. The script automatically installs required packages (Pillow, pillow-heif) on first run.

## Supported Formats

- JPEG/JPG
- PNG
- TIFF
- HEIC
- WebP

## Quick Start

The skill is installed at `~/.claude/skills/image-editor/`. The main editing script is at `~/.claude/skills/image-editor/scripts/edit_image.py`.

It uses uv for dependency management and automatically installs required packages when first run.

**IMPORTANT: Run the script using absolute paths (do NOT cd to any directory first):**

Basic usage:
```bash
uv run ~/.claude/skills/image-editor/scripts/edit_image.py /path/to/input.jpg /path/to/output.png [options]
```

## Common Operations

### Format Conversion

Convert between any supported formats by specifying different input/output extensions:

```bash
# JPEG to PNG (using absolute paths)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py ~/input/image.jpg ~/output/image.png

# PNG to WebP
uv run ~/.claude/skills/image-editor/scripts/edit_image.py ~/input/image.png ~/output/image.webp

# HEIC to JPEG
uv run ~/.claude/skills/image-editor/scripts/edit_image.py ~/input/image.heic ~/output/image.jpg
```

### Rotation

Rotate images by any angle (commonly 90, 180, 270 degrees):

```bash
# Rotate 90 degrees clockwise
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --rotate 90

# Rotate 180 degrees
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --rotate 180
```

### Resize

Resize images with or without aspect ratio preservation:

```bash
# Resize to 800x600, maintaining aspect ratio (fits within bounds)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --width 800 --height 600 --keep-aspect

# Resize to exact dimensions (may distort)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --width 800 --height 600

# Resize width only, maintaining aspect ratio
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --width 800 --keep-aspect
```

### Color Adjustments

Adjust brightness, contrast, and saturation using multiplier factors:

```bash
# Increase brightness by 20% (factor = 1.2)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --brightness 1.2

# Decrease brightness by 20% (factor = 0.8)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --brightness 0.8

# Increase contrast
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --contrast 1.3

# Increase saturation
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --saturation 1.2
```

### Transparency Handling

Replace transparent areas with a solid color:

```bash
# Replace transparency with white (default)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.png output.png --replace-transparency 255,255,255

# Replace transparency with black
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.png output.png --replace-transparency 0,0,0

# Replace transparency with custom color (R,G,B format)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.png output.png --replace-transparency 200,200,200
```

### Flip

Flip images horizontally or vertically:

```bash
# Flip horizontally (mirror)
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --flip horizontal

# Flip vertically
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --flip vertical
```

## Chaining Operations

Combine multiple operations in a single command. Operations are applied in this order:
1. Transparency replacement
2. Geometric transformations (rotate, flip, resize)
3. Color adjustments (brightness, contrast, saturation)

```bash
# Rotate 90 degrees and increase brightness by 20%
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.jpg --rotate 90 --brightness 1.2

# Resize, adjust colors, and convert format
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.jpg output.png --width 800 --height 600 --keep-aspect --brightness 1.1 --saturation 1.2

# Replace transparency, resize, and save as JPEG
uv run ~/.claude/skills/image-editor/scripts/edit_image.py input.png output.jpg --replace-transparency 255,255,255 --width 1024 --keep-aspect
```

## Workflow Guidelines

1. **Use absolute paths throughout** - Do NOT change directories with `cd`
2. **Input files**: Provide the full path to the input image file
3. **Run the script**: Use `uv run ~/.claude/skills/image-editor/scripts/edit_image.py` with absolute paths for input and output
4. **Output files**: Save to the desired output location with full path
5. **Provide file path**: Give user the path to the output file

Example:
```bash
uv run ~/.claude/skills/image-editor/scripts/edit_image.py ~/input/image.png ~/output/edited_image.png --rotate 90
```

## All Available Options

```
--format             Target format (JPEG, PNG, TIFF, HEIC, WEBP)
--rotate DEGREES     Rotation angle (e.g., 90, 180, 270, or any angle)
--width PIXELS       Target width in pixels
--height PIXELS      Target height in pixels
--keep-aspect        Maintain aspect ratio when resizing
--flip DIRECTION     Flip horizontal or vertical
--brightness FACTOR  Brightness multiplier (>1.0 brightens, <1.0 darkens)
--contrast FACTOR    Contrast multiplier (>1.0 increases, <1.0 decreases)
--saturation FACTOR  Saturation multiplier (>1.0 increases, <1.0 decreases)
--replace-transparency R,G,B  Replace transparency with color (e.g., 255,255,255)
```

## Notes

- **Always use absolute paths** - Do NOT use `cd` commands. Run the script with full absolute paths for input, output, and script location.
- JPEG format does not support transparency. When saving as JPEG, any transparency is automatically replaced with white.
- The `--keep-aspect` flag ensures images are not distorted when resizing. The output dimensions may be smaller than specified to maintain the aspect ratio.
- Color adjustment factors are multipliers: 1.0 = no change, >1.0 = increase, <1.0 = decrease.
- When chaining operations, order matters internally but the script handles the logical sequence automatically.
