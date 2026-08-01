
def __color_reduce(c):
    assert isinstance(c, Color)
    return __color_constructor, (c.r, c.g, c.b, c.a)

