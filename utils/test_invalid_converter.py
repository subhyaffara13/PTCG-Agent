
def test_invalid_converter(conv):
    msg = (
        "converters must be a dictionary mapping columns to converter "
        "functions or a single callable."
    )
    with pytest.raises(TypeError, match=msg):
        np.loadtxt(StringIO("1 2\n3 4"), converters=conv)

