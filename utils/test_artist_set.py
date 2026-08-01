
def test_artist_set():
    line = mlines.Line2D([], [])
    line.set(linewidth=7)
    assert line.get_linewidth() == 7

    # Property aliases should work
    line.set(lw=5)
    assert line.get_linewidth() == 5

