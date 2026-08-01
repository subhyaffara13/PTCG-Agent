
def test_numba_vs_python_reductions(reduction, apply_axis):
    df = DataFrame(np.ones((4, 4), dtype=np.float64))
    result = df.apply(reduction, engine="numba", axis=apply_axis)
    expected = df.apply(reduction, engine="python", axis=apply_axis)
    tm.assert_series_equal(result, expected)

