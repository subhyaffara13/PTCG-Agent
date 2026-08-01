
def test_ft2font_valid_args():
    class PathLikeClass:
        def __init__(self, filename):
            self.filename = filename

        def __fspath__(self):
            return self.filename

    file_str = fm.findfont('DejaVu Sans')
    file_bytes = os.fsencode(file_str)

    font = ft2font.FT2Font(file_str)
    assert font.fname == file_str
    font = ft2font.FT2Font(file_bytes)
    assert font.fname == file_bytes
    font = ft2font.FT2Font(PathLikeClass(file_str))
    assert font.fname == file_str
    font = ft2font.FT2Font(PathLikeClass(file_bytes))
    assert font.fname == file_bytes

