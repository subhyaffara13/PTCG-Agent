
def test_reduction_axis_none_returns_scalar(method, numeric_only, dtype):
    # GH#21597 As of 2.0, axis=None reduces over all axes.

    df = DataFrame(np.random.default_rng(2).standard_normal((4, 4)), dtype=dtype)

    result = getattr(df, method)(axis=None, numeric_only=numeric_only)
    np_arr = df.to_numpy(dtype=np.float64)
    if method in {"skew", "kurt"}:
        comp_mod = pytest.importorskip("scipy.stats")
        if method == "kurt":
            method = "kurtosis"
        expected = getattr(comp_mod, method)(np_arr, bias=False, axis=None)
        tm.assert_almost_equal(result, expected)
    else:
        expected = getattr(np, method)(np_arr, axis=None)
        assert result == expected

