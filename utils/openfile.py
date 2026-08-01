
def openfile(fname):
    """
    Opens the file handle of file `fname`.

    """
    # A file handle
    if hasattr(fname, 'readline'):
        return fname
    # Try to open the file and guess its type
    try:
        f = open(fname)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file: '{fname}'") from e
    if f.readline()[:2] != "\\x":
        f.seek(0, 0)
        return f
    f.close()
    raise NotImplementedError("Wow, binary file")

