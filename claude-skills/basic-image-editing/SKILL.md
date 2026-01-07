---
name: basic-image-editing
description: Basic image editing operations including rotation, flipping, resizing, transparency handling, format conversion, padding, cropping, file size reduction, metadata retrieval, grayscale conversion, alpha mask extraction, alpha blending, and auto-cropping transparent borders. Use when Claude needs to perform image transformations such as rotating images by any angle, flipping horizontally or vertically, resizing with flexible dimension handling, removing or replacing transparency, converting between formats (JPEG, PNG, WebP, TIFF, HEIC), adding padding with solid colors or edge replication, cropping from any side, reducing file size to a target, getting image metadata, converting to grayscale, extracting alpha masks, applying masks via alpha blending, or auto-cropping transparent borders.
---

# Basic Image Editing

Perform image transformations using `scripts/image_edit.py`.

## Quick Start

```bash
uv run scripts/image_edit.py INPUT -o OUTPUT [options]
```

## Operations

### Image Info

```bash
uv run scripts/image_edit.py input.png --info
```

Displays: dimensions, format, file size, color mode, DPI.

### Rotate

```bash
uv run scripts/image_edit.py input.png -o output.png --rotate 90
uv run scripts/image_edit.py input.png -o output.png --rotate 45
```

### Flip

```bash
uv run scripts/image_edit.py input.png -o output.png --flip horizontal
uv run scripts/image_edit.py input.png -o output.png --flip vertical
```

### Resize

```bash
# Exact dimensions
uv run scripts/image_edit.py input.png -o output.png --width 800 --height 600

# Width only (maintains aspect ratio)
uv run scripts/image_edit.py input.png -o output.png --width 800

# Height only (maintains aspect ratio)
uv run scripts/image_edit.py input.png -o output.png --height 600
```

### Format Conversion

Convert by specifying output extension:

```bash
uv run scripts/image_edit.py input.png -o output.webp
uv run scripts/image_edit.py input.heic -o output.jpg
```

Supported: JPEG, PNG, WebP, TIFF, HEIC/HEIF.

### Grayscale

```bash
uv run scripts/image_edit.py input.png -o output.png --grayscale
```

Converts to single-channel grayscale (mode 'L').

### Transparency

```bash
# Remove alpha (white background)
uv run scripts/image_edit.py input.png -o output.jpg --remove-transparency

# Replace with color
uv run scripts/image_edit.py input.png -o output.png --replace-transparency red
uv run scripts/image_edit.py input.png -o output.png --replace-transparency "#FF5500"
```

If image has no alpha channel, prints a note and continues.

### Extract Alpha Mask

```bash
uv run scripts/image_edit.py input.png -o mask.png --extract-mask
```

Extracts the alpha channel as a 1-channel grayscale mask. Requires RGBA image.

### Alpha Blend (Apply Mask)

```bash
uv run scripts/image_edit.py input.png -o output.png --mask mask.png
```

Applies a grayscale mask as the alpha channel, creating an RGBA composite. Mask is automatically resized to match image dimensions if needed.

### Auto-Crop Transparency

```bash
uv run scripts/image_edit.py input.png -o output.png --autocrop-transparency 0
uv run scripts/image_edit.py input.png -o output.png --autocrop-transparency 5
```

Crops transparent borders from image. Threshold (0-100%) controls which pixels are considered transparent:
- `0` = only fully transparent pixels (alpha=0)
- `5` = pixels with alpha < 5% (≈12/255)
- `100` = all pixels considered transparent

### Padding

```bash
# All sides equal
uv run scripts/image_edit.py input.png -o output.png --pad 20

# Vertical, horizontal
uv run scripts/image_edit.py input.png -o output.png --pad 10,20

# Top, right, bottom, left
uv run scripts/image_edit.py input.png -o output.png --pad 10,20,30,40

# With color
uv run scripts/image_edit.py input.png -o output.png --pad 20 --pad-color blue

# Edge pixel replication
uv run scripts/image_edit.py input.png -o output.png --pad 20 --pad-edge
```

### Cropping

```bash
# All sides equal
uv run scripts/image_edit.py input.png -o output.png --crop 50

# Top, right, bottom, left
uv run scripts/image_edit.py input.png -o output.png --crop 10,20,30,40
```

### File Size Reduction

```bash
uv run scripts/image_edit.py input.png -o output.jpg --max-size 1
uv run scripts/image_edit.py input.png -o output.webp --max-size 0.5
```

Uses binary search to find optimal quality/dimensions.

## Color Formats

| Format | Examples |
|--------|----------|
| Named | `red`, `blue`, `coral`, `darkslategray` (140+ CSS colors) |
| Hex | `#RGB`, `#RRGGBB`, `#RRGGBBAA` |
| RGB | `255,128,0` or `rgb(255,128,0)` |
| HSL | `hsl(120,100%,50%)` |

## Combining Operations

Operations apply in order: rotate → flip → autocrop → crop → resize → pad → mask → grayscale → transparency.

```bash
uv run scripts/image_edit.py input.png -o output.jpg \
    --rotate 90 \
    --autocrop-transparency 5 \
    --width 800 \
    --pad 20 --pad-color white
```
