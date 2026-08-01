
def test_valid_drawstyles():
    line = mlines.Line2D([], [])
    with pytest.raises(ValueError):
        line.set_drawstyle('foobar')

