
def test_getattr():
    A = Matrix(((1, 4, x), (y, 2, 4), (10, 5, x**2 + 1)))
    raises(AttributeError, lambda: A.nonexistantattribute)
    assert getattr(A, 'diff')(x) == Matrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))


def test_getattr():
    A = Matrix(((1, 4, x), (y, 2, 4), (10, 5, x**2 + 1)))
    raises(AttributeError, lambda: A.nonexistantattribute)
    assert getattr(A, 'diff')(x) == Matrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))


def test_getattr(temp_hdfstore):
    store = temp_hdfstore
    s = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    store["a"] = s

    # test attribute access
    result = store.a
    tm.assert_series_equal(result, s)
    result = store.a
    tm.assert_series_equal(result, s)

    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    store["df"] = df
    result = store.df
    tm.assert_frame_equal(result, df)

    # errors
    for x in ["d", "mode", "path", "handle", "complib"]:
        msg = f"'HDFStore' object has no attribute '{x}'"
        with pytest.raises(AttributeError, match=msg):
            getattr(store, x)

    # not stores
    for x in ["mode", "path", "handle", "complib"]:
        getattr(store, f"_{x}")


def test_getattr(module_name):
    _test_getattr(module_name)

