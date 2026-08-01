
def __rect_reduce(r):
    assert isinstance(r, Rect)
    return __rect_constructor, (r.x, r.y, r.w, r.h)

