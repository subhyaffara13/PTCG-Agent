
def test_use_global_config():
    def f(x):
        return np.mean(x) + 2

    s = Series(range(10))
    with option_context("compute.use_numba", True):
        result = s.rolling(2).apply(f, engine=None, raw=True)
    expected = s.rolling(2).apply(f, engine="numba", raw=True)
    tm.assert_series_equal(expected, result)


def test_use_global_config():
    pytest.importorskip("numba")

    def func_1(values, index):
        return np.mean(values) - 3.4

    data = DataFrame(
        {0: ["a", "a", "b", "b", "a"], 1: [1.0, 2.0, 3.0, 4.0, 5.0]}, columns=[0, 1]
    )
    grouped = data.groupby(0)
    expected = grouped.agg(func_1, engine="numba")
    with option_context("compute.use_numba", True):
        result = grouped.agg(func_1, engine=None)
    tm.assert_frame_equal(expected, result)


def test_use_global_config():
    pytest.importorskip("numba")

    def func_1(values, index):
        return values + 1

    data = DataFrame(
        {0: ["a", "a", "b", "b", "a"], 1: [1.0, 2.0, 3.0, 4.0, 5.0]}, columns=[0, 1]
    )
    grouped = data.groupby(0)
    expected = grouped.transform(func_1, engine="numba")
    with option_context("compute.use_numba", True):
        result = grouped.transform(func_1, engine=None)
    tm.assert_frame_equal(expected, result)

