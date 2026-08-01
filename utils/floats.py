
def floats(*args, **kwargs):
    if 'width' not in kwargs:
        kwargs['width'] = 32
    return _floats_wrapper(*args, **kwargs)

