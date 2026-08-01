
def test_valid_linestyles():
    line = mlines.Line2D([], [])
    with pytest.raises(ValueError):
        line.set_linestyle('aardvark')

