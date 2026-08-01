
def isbase(path1: str, path2: str) -> bool:
    # Check if `path1` is a base or prefix of `path2`.
    _path1 = forcedir(abspath(path1))
    _path2 = forcedir(abspath(path2))
    return _path2.startswith(_path1)

