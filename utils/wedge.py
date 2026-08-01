
def wedge(mode: str = "RGB") -> ImagePalette:
    palette = list(range(256 * len(mode)))
    return ImagePalette(mode, [i // len(mode) for i in palette])

