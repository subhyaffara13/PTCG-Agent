
def test_skiprow_exceeding_maxrows_exceeding_chunksize(tmpdir, nskip):
    # tries to read a file in chunks by skipping a variable amount of lines,
    # less, equal, greater than max_rows
    file_length = 110000
    data = "\n".join(f"{i} a 0.5 1" for i in range(1, file_length + 1))
    expected_length = min(60000, file_length - nskip)
    expected = np.arange(nskip + 1, nskip + 1 + expected_length).astype(str)

    # file-like path
    txt = StringIO(data)
    res = np.loadtxt(txt, dtype='str', delimiter=" ", skiprows=nskip, max_rows=60000)
    assert len(res) == expected_length
    # are the right lines read in res?
    assert_array_equal(expected, res[:, 0])

    # file-obj path
    tmp_file = tmpdir / "test_data.txt"
    tmp_file.write(data)
    fname = str(tmp_file)
    res = np.loadtxt(fname, dtype='str', delimiter=" ", skiprows=nskip, max_rows=60000)
    assert len(res) == expected_length
    # are the right lines read in res?
    assert_array_equal(expected, res[:, 0])

