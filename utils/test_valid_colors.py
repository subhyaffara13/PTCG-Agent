
def test_valid_colors():
    line = mlines.Line2D([], [])
    with pytest.raises(ValueError):
        line.set_color("foobar")

