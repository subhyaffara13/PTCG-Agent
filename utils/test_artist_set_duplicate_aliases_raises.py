
def test_artist_set_duplicate_aliases_raises():
    """
    Test that set() raises TypeError when both a property and its alias are provided.
    """
    line = mlines.Line2D([0, 1], [0, 1])

    with pytest.raises(TypeError, match="aliases of one another"):
        line.set(lw=2, linewidth=3)

