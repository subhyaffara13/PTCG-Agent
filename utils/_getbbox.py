
def _getbbox(
    base_im: Image.Image, im_frame: Image.Image
) -> tuple[Image.Image, tuple[int, int, int, int] | None]:
    palette_bytes = [
        bytes(im.palette.palette) if im.palette else b"" for im in (base_im, im_frame)
    ]
    if palette_bytes[0] != palette_bytes[1]:
        im_frame = im_frame.convert("RGBA")
        base_im = base_im.convert("RGBA")
    delta = ImageChops.subtract_modulo(im_frame, base_im)
    return delta, delta.getbbox(alpha_only=False)

