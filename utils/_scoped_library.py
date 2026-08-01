
def _scoped_library(*args, **kwargs):
    try:
        lib = Library(*args, **kwargs)
        yield lib
    finally:
        lib._destroy()

