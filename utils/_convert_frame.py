
def _convert_frame(im: Image.Image) -> Image.Image:
    # Make sure image mode is supported
    if im.mode not in ("RGBX", "RGBA", "RGB"):
        im = im.convert("RGBA" if im.has_transparency_data else "RGB")
    return im

