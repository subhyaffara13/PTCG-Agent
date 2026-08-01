
def test_multifunc_numba_kwarg_propagation(data, agg_kwargs):
    pytest.importorskip("numba")
    labels = ["a", "a", "b", "b", "a"]
    grouped = data.groupby(labels)
    result = grouped.agg(**agg_kwargs, engine="numba", engine_kwargs={"parallel": True})
    expected = grouped.agg(**agg_kwargs, engine="numba")
    if isinstance(expected, DataFrame):
        tm.assert_frame_equal(result, expected)
    else:
        tm.assert_series_equal(result, expected)

