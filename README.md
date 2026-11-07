# Bite v0.1.0

Bite is a lightweight Python library for managing binary sprites and color palettes, resizing sprites, and converting them into XBM data for use with Tkinter.

Define your sprites using 2D arrays of `0`s and `1`s, store them under unique IDs, and resize them to fit the pixel space you need.

## Features

- Store multiple sprites under unique IDs.
- Define sprites using 2D arrays of binary integers.
- Store reusable foreground and background palettes.
- Resize sprites to an exact width and height using nearest-neighbor sampling.
- Convert sprite structures into XBM strings without writing XBM files.
- No third-party dependencies or Tkinter imports inside Bite.

Bite handles data. Your application creates and displays the images.

## Setup

Place the package folder alongside your application:

- `bite/__init__.py`
- `bite/bite.py`
- `main.py`

Then import Bite:

```python
from bite import Bite
```

Bite itself uses standard Python features and requires no additional packages. The example below requires a Python installation with Tkinter available.

## Quick Start

```python
from bite import Bite

sprite_manager = Bite(
	structures={
		"house": [
			[0, 0, 1, 0, 0],
			[0, 1, 1, 1, 0],
			[1, 1, 1, 1, 1],
			[0, 1, 0, 1, 0],
			[0, 1, 1, 1, 0],
		],
	},
	palettes={
		"parchment": {
			"foreground": "#69432b",
			"background": "#f3dfac",
		},
	},
)

sprite = sprite_manager.get_sprite("house")
palette = sprite_manager.get_palette("parchment")

resized_sprite = sprite.resize(width=150, height=150)
bitmap_data = resized_sprite.to_xbm()
```

## Using Bite with Tkinter

This complete example creates a sprite, applies a palette, and displays a resized bitmap on a canvas.

```python
from tkinter import Tk, Canvas, BitmapImage, BOTH
from bite import Bite

root = Tk()
root.title("Bite Demo")

canvas = Canvas(root, width=500, height=500)
canvas.pack(fill=BOTH, expand=True)

sprite_manager = Bite()

sprite_manager.add_sprite("house", [
	[0, 0, 1, 0, 0],
	[0, 1, 1, 1, 0],
	[1, 1, 1, 1, 1],
	[0, 1, 0, 1, 0],
	[0, 1, 1, 1, 0],
])

sprite_manager.add_palette(
	"parchment",
	foreground="#69432b",
	background="#f3dfac",
)

sprite = sprite_manager.get_sprite("house")
palette = sprite_manager.get_palette("parchment")
resized_sprite = sprite.resize(150, 150)

image = BitmapImage(
	master=root,
	data=resized_sprite.to_xbm(),
	foreground=palette.foreground,
	background=palette.background,
)

canvas.create_image(250, 250, image=image)

root.mainloop()
```

Keep a Python reference to each `BitmapImage` while it is displayed. For multiple images, you can store references in a list or dictionary.

## Sprite Structures

Each inner list represents one row. All rows must have the same length, and every value must be the integer `0` or `1`.

- `1` uses the image's foreground color.
- `0` uses the image's background color.

Empty structures, uneven rows, and values other than integer `0` or `1` raise `ValueError`.

Bite copies the supplied rows when creating a sprite, so later changes to the original input array do not change the stored sprite.

## Palettes

Palettes store color strings independently of sprites. The same sprite can be displayed with multiple palettes, and the same palette can be used with multiple sprites.

```python
sprite_manager.add_palette(
	"night",
	foreground="lightblue",
	background="midnightblue",
)

sprite_manager.add_palette(
	"transparent",
	foreground="darkgreen",
	background="",
)
```

Use an empty background string for transparent `0` pixels in Tkinter. Colors are passed through unchanged; Tkinter validates them when they are applied to an image.

To change an existing Tkinter image's palette:

```python
palette = sprite_manager.get_palette("night")

image.configure(
	foreground=palette.foreground,
	background=palette.background,
)
```

Palette colors are supplied separately to `BitmapImage`; they are not embedded in the XBM string. Changing a stored palette does not automatically update existing images.

## Resizing

```python
sprite = sprite_manager.get_sprite("house")
resized_sprite = sprite.resize(width=200, height=100)
```

`resize()` returns a new sprite and leaves the original unchanged. Width and height must be positive integers.

The sprite is stretched to exactly the requested dimensions. Each axis scales independently, so the original aspect ratio is not automatically preserved. Nearest-neighbor sampling keeps all pixels binary, although shrinking can remove small details.

For repeated resizing, start from the original sprite rather than a previously resized version.

## API Reference

### Bite

| Method | Description |
| --- | --- |
| `Bite(structures=None, palettes=None)` | Create a manager, optionally with dictionaries of sprite structures and palette settings. |
| `add_sprite(sprite_id, structure)` | Create, store, and return a sprite. |
| `get_sprite(sprite_id)` | Return a stored sprite. |
| `add_palette(palette_id, foreground="black", background="")` | Create, store, and return a palette. |
| `get_palette(palette_id)` | Return a stored palette. |

Sprite IDs must be unique within `sprites`; palette IDs must be unique within `palettes`. The same ID can appear in both collections. Duplicate IDs raise `ValueError`; requesting a missing ID raises `KeyError`.

### Sprite

Sprite objects are created and returned by Bite.

| Attribute or method | Description |
| --- | --- |
| `structure` | The stored 2D array of binary pixels. |
| `width` | Width of the sprite in pixels. |
| `height` | Height of the sprite in pixels. |
| `resize(width, height)` | Return a new sprite at the requested dimensions. |
| `to_xbm()` | Return an XBM-formatted string for the sprite. |

### Palette

Palette objects are created and returned by Bite.

| Attribute | Description |
| --- | --- |
| `foreground` | Color used for `1` pixels. Defaults to `"black"`. |
| `background` | Color used for `0` pixels. Defaults to `""`. |
