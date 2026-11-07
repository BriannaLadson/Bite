class Bite:
	def __init__(self, structures=None, palettes=None):
		self.sprites = {}
		self.palettes = {}

		if structures is not None:
			for sprite_id, structure in structures.items():
				self.add_sprite(sprite_id, structure)

		if palettes is not None:
			for palette_id, colors in palettes.items():
				self.add_palette(palette_id, **colors)

	def add_sprite(self, sprite_id, structure):
		if sprite_id in self.sprites:
			raise ValueError(f"Sprite ID {sprite_id!r} already exists.")

		sprite = Sprite(structure)
		self.sprites[sprite_id] = sprite

		return sprite

	def get_sprite(self, sprite_id):
		return self.sprites[sprite_id]

	def add_palette(self, palette_id, foreground="black", background=""):
		if palette_id in self.palettes:
			raise ValueError(f"Palette ID {palette_id!r} already exists.")

		palette = Palette(foreground, background)
		self.palettes[palette_id] = palette

		return palette

	def get_palette(self, palette_id):
		return self.palettes[palette_id]
		
class Sprite:
	def __init__(self, structure):
		if not structure or not structure[0]:
			raise ValueError("The sprite cannot be empty.")

		width = len(structure[0])

		for row in structure:
			if len(row) != width:
				raise ValueError("All rows must have the same length.")

			for pixel in row:
				if type(pixel) is not int or pixel not in (0, 1):
					raise ValueError("Pixels must be integers: 0 or 1.")

		self.structure = [list(row) for row in structure]
		self.width = width
		self.height = len(structure)
		
	def to_xbm(self):
		values = []

		for row in self.structure:
			for start in range(0, self.width, 8):
				byte = 0

				for offset, pixel in enumerate(row[start:start + 8]):
					byte |= pixel << offset

				values.append(f"0x{byte:02x}")

		return (
			f"#define sprite_width {self.width}\n"
			f"#define sprite_height {self.height}\n"
			"static unsigned char sprite_bits[] = {\n"
			+ ", ".join(values)
			+ "\n};"
		)
		
	def resize(self, width, height):
		if type(width) is not int or type(height) is not int:
			raise ValueError("Width and height must be integers.")

		if width <= 0 or height <= 0:
			raise ValueError("Width and height must be greater than zero.")

		structure = []

		for y in range(height):
			source_y = y * self.height // height
			row = []

			for x in range(width):
				source_x = x * self.width // width
				pixel = self.structure[source_y][source_x]
				row.append(pixel)

			structure.append(row)

		return Sprite(structure)
		
class Palette:
	def __init__(self, foreground="black", background=""):
		self.foreground = foreground
		self.background = background