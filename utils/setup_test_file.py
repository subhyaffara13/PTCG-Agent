
def setup_test_file():
    val = b'a\x00string'
    fd, fname = mkstemp()

    with os.fdopen(fd, 'wb') as fs:
        fs.write(val)
    with open(fname, 'rb') as fs:
        gs = BytesIO(val)
        cs = BytesIO(val)
        yield fs, gs, cs
    os.unlink(fname)

