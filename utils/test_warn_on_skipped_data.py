
def test_warn_on_skipped_data(skiprows):
    data = "1 2 3\n4 5 6"
    txt = StringIO(data)
    with pytest.warns(UserWarning, match="input contained no data"):
        np.loadtxt(txt, skiprows=skiprows)

