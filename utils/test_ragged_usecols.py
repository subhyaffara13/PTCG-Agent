
def test_ragged_usecols():
    # usecols, and negative ones, work even with varying number of columns.
    txt = StringIO("0,0,XXX\n0,XXX,0,XXX\n0,XXX,XXX,0,XXX\n")
    expected = np.array([[0, 0], [0, 0], [0, 0]])
    res = np.loadtxt(txt, dtype=float, delimiter=",", usecols=[0, -2])
    assert_equal(res, expected)

    txt = StringIO("0,0,XXX\n0\n0,XXX,XXX,0,XXX\n")
    with pytest.raises(ValueError,
                match="invalid column index -2 at row 2 with 1 columns"):
        # There is no -2 column in the second row:
        np.loadtxt(txt, dtype=float, delimiter=",", usecols=[0, -2])

