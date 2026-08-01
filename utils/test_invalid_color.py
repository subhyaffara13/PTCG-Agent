
def test_invalid_color():
    with pytest.raises(ValueError):
        plt.figtext(.5, .5, "foo", c="foobar")

