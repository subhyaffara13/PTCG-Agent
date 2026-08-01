
def test_min_max(A):
    # Some formats don't support min/max operations, so we skip those here.
    if hasattr(A, 'min'):
        assert not isinstance(A.min(axis=1), np.matrix), \
            "Expected array, got matrix"
    if hasattr(A, 'max'):
        assert not isinstance(A.max(axis=1), np.matrix), \
            "Expected array, got matrix"
    if hasattr(A, 'argmin'):
        assert not isinstance(A.argmin(axis=1), np.matrix), \
            "Expected array, got matrix"
    if hasattr(A, 'argmax'):
        assert not isinstance(A.argmax(axis=1), np.matrix), \
            "Expected array, got matrix"


def test_min_max(shape, axis):
    rng = np.random.default_rng(23409823)
    a = random_array(shape, density=0.6, random_state=rng, dtype=int)

    res_min = a.min(axis=axis)
    exp_min = np.min(a.toarray(), axis=axis)
    res_max = a.max(axis=axis)
    exp_max = np.max(a.toarray(), axis=axis)
    res_nanmin = a.nanmin(axis=axis)
    exp_nanmin = np.nanmin(a.toarray(), axis=axis)
    res_nanmax = a.nanmax(axis=axis)
    exp_nanmax = np.nanmax(a.toarray(), axis=axis)

    for res, exp in [(res_min, exp_min), (res_max, exp_max),
                     (res_nanmin, exp_nanmin), (res_nanmax, exp_nanmax)]:
        if np.issubdtype(type(res), np.number):
            assert_equal(res, exp)
        else:
            assert_equal(res.toarray(), exp)


def test_min_max(method, skipna, dtype):
    arr = pd.Series(["a", "b", "c", None], dtype=dtype)
    result = getattr(arr, method)(skipna=skipna)
    if skipna:
        expected = "a" if method == "min" else "c"
        assert result == expected
    else:
        assert result is arr.dtype.na_value

