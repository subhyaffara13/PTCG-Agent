
def _handle(f, *args, **kwargs):
    handle = f(*args, **kwargs)
    try:
        yield handle
    finally:
        kernel32.CloseHandle(handle)

