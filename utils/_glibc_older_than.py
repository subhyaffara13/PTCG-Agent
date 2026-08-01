
def _glibc_older_than(x):
    return _glibcver != "0.0" and _glibcver < x

