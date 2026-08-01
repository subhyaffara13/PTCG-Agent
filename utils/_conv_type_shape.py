
def _conv_type_shape(im: Image) -> tuple[tuple[int, ...], str]:
    m = ImageMode.getmode(im.mode)
    shape: tuple[int, ...] = (im.height, im.width)
    extra = len(m.bands)
    if extra != 1:
        shape += (extra,)
    return shape, m.typestr

