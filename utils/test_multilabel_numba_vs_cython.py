
def test_multilabel_numba_vs_cython(numba_supported_reductions):
    pytest.importorskip("numba")
    reduction, kwargs = numba_supported_reductions
    df = DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.default_rng(2).standard_normal(8),
            "D": np.random.default_rng(2).standard_normal(8),
        }
    )
    gb = df.groupby(["A", "B"])
    res_agg = gb.agg(reduction, engine="numba", **kwargs)
    expected_agg = gb.agg(reduction, engine="cython", **kwargs)
    tm.assert_frame_equal(res_agg, expected_agg)
    # Test that calling the aggregation directly also works
    direct_res = getattr(gb, reduction)(engine="numba", **kwargs)
    direct_expected = getattr(gb, reduction)(engine="cython", **kwargs)
    tm.assert_frame_equal(direct_res, direct_expected)


def test_multilabel_numba_vs_cython(numba_supported_reductions):
    pytest.importorskip("numba")
    reduction, kwargs = numba_supported_reductions
    df = DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.default_rng(2).standard_normal(8),
            "D": np.random.default_rng(2).standard_normal(8),
        }
    )
    gb = df.groupby(["A", "B"])
    res_agg = gb.transform(reduction, engine="numba", **kwargs)
    expected_agg = gb.transform(reduction, engine="cython", **kwargs)
    tm.assert_frame_equal(res_agg, expected_agg)

