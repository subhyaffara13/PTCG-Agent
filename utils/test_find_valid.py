
def test_find_valid():
    class PathLikeClass:
        def __init__(self, filename):
            self.filename = filename

        def __fspath__(self):
            return self.filename

    file_str = findfont('DejaVu Sans')
    file_bytes = os.fsencode(file_str)

    font = get_font(file_str)
    assert font.fname == file_str
    font = get_font(file_bytes)
    assert font.fname == file_bytes
    font = get_font(PathLikeClass(file_str))
    assert font.fname == file_str
    font = get_font(PathLikeClass(file_bytes))
    assert font.fname == file_bytes
    font = get_font(FontPath(file_str, 0))
    assert font.fname == file_str

    # Note, fallbacks are not currently accessible.
    font = get_font([file_str, file_bytes,
                     PathLikeClass(file_str), PathLikeClass(file_bytes)])
    assert font.fname == file_str

