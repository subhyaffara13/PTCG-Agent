
def test_gh_28206():
    a = np.arange(3)
    b = np.ones((3, 3), dtype=np.int64)
    out = np.array([np.nan, np.nan, np.nan])

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        np.choose(a, b, out=out)

