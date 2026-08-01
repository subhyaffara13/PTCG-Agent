
def compare_results(res, desired):
    """Compare lists of arrays."""
    for x, y in zip(res, desired, strict=False):
        assert_array_equal(x, y)

