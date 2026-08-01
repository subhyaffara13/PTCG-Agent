
def test_artist_set_invalid_property_raises():
    """
    Test that set() raises AttributeError for invalid property names.
    """
    line = mlines.Line2D([0, 1], [0, 1])

    with pytest.raises(AttributeError, match="unexpected keyword argument"):
        line.set(not_a_property=1)

