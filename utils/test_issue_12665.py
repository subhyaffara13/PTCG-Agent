
def test_issue_12665():
    # Testing Python 3 hash of immutable arrays:
    arr = ImmutableDenseNDimArray([1, 2, 3])
    # This should NOT raise an exception:
    hash(arr)

