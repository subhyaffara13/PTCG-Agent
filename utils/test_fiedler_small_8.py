
def test_fiedler_small_8():
    """Check the dense workaround path for small matrices.
    """
    # This triggers the dense path because 8 < 2*5.
    with pytest.warns(UserWarning, match="The problem size"):
        _check_fiedler(8, 2)

