
def test_warn_on_no_data(data, ndmin, usecols):
    """Check that a UserWarning is emitted when no data is read from input."""
    if usecols is not None:
        expected_shape = (0, 3)
    elif ndmin == 2:
        expected_shape = (0, 1)  # guess a single column?!
    else:
        expected_shape = (0,)

    txt = StringIO(data)
    with pytest.warns(UserWarning, match="input contained no data"):
        res = np.loadtxt(txt, ndmin=ndmin, usecols=usecols)
    assert res.shape == expected_shape

    with NamedTemporaryFile(mode="w") as fh:
        fh.write(data)
        fh.seek(0)
        with pytest.warns(UserWarning, match="input contained no data"):
            res = np.loadtxt(txt, ndmin=ndmin, usecols=usecols)
        assert res.shape == expected_shape

