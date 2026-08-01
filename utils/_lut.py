
def _lut(image: Image.Image, lut: list[int]) -> Image.Image:
    if image.mode == "P":
        # FIXME: apply to lookup table, not image data
        msg = "mode P support coming soon"
        raise NotImplementedError(msg)
    elif image.mode in ("L", "RGB"):
        if image.mode == "RGB" and len(lut) == 256:
            lut = lut + lut + lut
        return image.point(lut)
    else:
        msg = f"not supported for mode {image.mode}"
        raise OSError(msg)

