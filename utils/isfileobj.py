
def isfileobj(f):
    if not isinstance(f, (io.FileIO, io.BufferedReader, io.BufferedWriter)):
        return False
    try:
        # BufferedReader/Writer may raise OSError when
        # fetching `fileno()` (e.g. when wrapping BytesIO).
        f.fileno()
        return True
    except OSError:
        return False

