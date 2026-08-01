
def _unmultiplied_rgba8888_to_premultiplied_argb32(rgba8888):
    """
    Convert an unmultiplied RGBA8888 buffer to a premultiplied ARGB32 buffer.
    """
    if sys.byteorder == "little":
        argb32 = np.take(rgba8888, [2, 1, 0, 3], axis=2)
        rgb24 = argb32[..., :-1]
        alpha8 = argb32[..., -1:]
    else:
        argb32 = np.take(rgba8888, [3, 0, 1, 2], axis=2)
        alpha8 = argb32[..., :1]
        rgb24 = argb32[..., 1:]
    # Only bother premultiplying when the alpha channel is not fully opaque,
    # as the cost is not negligible.  The unsafe cast is needed to do the
    # multiplication in-place in an integer buffer.
    if alpha8.min() != 0xff:
        np.multiply(rgb24, alpha8 / 0xff, out=rgb24, casting="unsafe")
    return argb32

