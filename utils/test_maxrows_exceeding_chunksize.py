
def test_maxrows_exceeding_chunksize(nmax):
    # tries to read all of the file,
    # or less, equal, greater than _loadtxt_chunksize
    file_length = 60000

    # file-like path
    data = ["a 0.5 1"] * file_length
    txt = StringIO("\n".join(data))
    res = np.loadtxt(txt, dtype=str, delimiter=" ", max_rows=nmax)
    assert len(res) == nmax

    # file-obj path
    fd, fname = mkstemp()
    os.close(fd)
    with open(fname, "w") as fh:
        fh.write("\n".join(data))
    res = np.loadtxt(fname, dtype=str, delimiter=" ", max_rows=nmax)
    os.remove(fname)
    assert len(res) == nmax

