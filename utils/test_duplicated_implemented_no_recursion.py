import sys

def test_duplicated_implemented_no_recursion():
    # gh-21524
    # Ensure duplicated isn't implemented using recursion that
    # can fail on wide frames
    df = DataFrame(np.random.default_rng(2).integers(0, 1000, (10, 1000)))
    rec_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(100)
        result = df.duplicated()
    finally:
        sys.setrecursionlimit(rec_limit)

    # Then duplicates produce the bool Series as a result and don't fail during
    # calculation. Actual values doesn't matter here, though usually it's all
    # False in this case
    assert isinstance(result, Series)
    assert result.dtype == np.bool_

