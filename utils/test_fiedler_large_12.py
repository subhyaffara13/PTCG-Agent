
def test_fiedler_large_12():
    """Check the dense workaround path avoided for non-small matrices.
    """
    # This does not trigger the dense path, because 2*5 <= 12.
    _check_fiedler(12, 2)

