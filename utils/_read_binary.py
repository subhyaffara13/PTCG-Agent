
def _read_binary(pkgname, filename):
    import sys

    if sys.version_info >= (3, 10):
        # files was added in Python 3.9 but only seems to work here in 3.10+
        from importlib.resources import files
        return files(pkgname).joinpath(filename).read_bytes()
    else:
        # read_binary was deprecated in Python 3.11
        from importlib.resources import read_binary
        return read_binary(pkgname, filename)

