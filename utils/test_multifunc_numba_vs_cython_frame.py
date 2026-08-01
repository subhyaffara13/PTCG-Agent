
def test_multifunc_numba_vs_cython_frame(agg_kwargs):
    pytest.importorskip("numba")
    data = DataFrame(
        {
            0: ["a", "a", "b", "b", "a"],
            1: [1.0, 2.0, 3.0, 4.0, 5.0],
            2: [1, 2, 3, 4, 5],
        },
        columns=[0, 1, 2],
    )
    grouped = data.groupby(0)
    result = grouped.agg(**agg_kwargs, engine="numba")
    expected = grouped.agg(**agg_kwargs, engine="cython")
    tm.assert_frame_equal(result, expected)

