
def test_nat_pinned_docstrings():
    # see gh-17327
    assert NaT.ctime.__doc__ == Timestamp.ctime.__doc__

