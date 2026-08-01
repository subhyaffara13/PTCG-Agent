
def _open_file_context(file_like, appendmat, mode='rb'):
    f, opened = _open_file(file_like, appendmat, mode)
    try:
        yield f
    finally:
        if opened:
            f.close()

