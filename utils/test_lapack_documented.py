
def test_lapack_documented():
    """Test that all entries are in the doc."""
    if lapack.__doc__ is None:  # just in case there is a python -OO
        pytest.skip('lapack.__doc__ is None')
    names = set(lapack.__doc__.split())
    ignore_list = {
        "absolute_import",
        "division",
        "find_best_lapack_type",
        "flapack",
        "print_function",
        "HAS_ILP64",
        "HAS_LP64",
        "np",
    }
    missing = list()
    for name in dir(lapack):
        if (not name.startswith('_') and name not in ignore_list and
                name not in names):
            missing.append(name)
    assert missing == [], 'Name(s) missing from lapack.__doc__ or ignore_list'

