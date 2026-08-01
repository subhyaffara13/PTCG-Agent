
def test_empty_indexing():
    """Regression test for ticket 1948."""
    # Check that indexing a chararray with an empty list/array returns an
    # empty chararray instead of a chararray with a single empty string in it.
    s = np.char.chararray((4,))
    assert_(s[[]].size == 0)

