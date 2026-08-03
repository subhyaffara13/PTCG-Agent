import os

def test_parametric_unit_discovery(
    generic_data, long_datum, unitless_dtype, expected_dtype, nrows
):
    """Check that the correct unit (e.g. month, day, second) is discovered from
    the data when a user specifies a unitless datetime."""
    # Unit should be "D" (days) due to last entry
    data = [generic_data] * nrows + [long_datum]
    expected = np.array(data, dtype=expected_dtype)
    assert len(data) == nrows + 1
    assert len(data) == len(expected)

    # file-like path
    txt = StringIO("\n".join(data))
    a = np.loadtxt(txt, dtype=unitless_dtype)
    assert len(a) == len(expected)
    assert a.dtype == expected.dtype
    assert_equal(a, expected)

    # file-obj path
    fd, fname = mkstemp()
    os.close(fd)
    with open(fname, "w") as fh:
        fh.write("\n".join(data) + "\n")
    # loading the full file...
    a = np.loadtxt(fname, dtype=unitless_dtype)
    assert len(a) == len(expected)
    assert a.dtype == expected.dtype
    assert_equal(a, expected)
    # loading half of the file...
    a = np.loadtxt(fname, dtype=unitless_dtype, max_rows=int(nrows / 2))
    os.remove(fname)
    assert len(a) == int(nrows / 2)
    assert_equal(a, expected[:int(nrows / 2)])

