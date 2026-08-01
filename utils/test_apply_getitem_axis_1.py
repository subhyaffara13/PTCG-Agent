
def test_apply_getitem_axis_1(engine, request):
    # GH 13427
    if engine == "numba":
        mark = pytest.mark.xfail(
            reason="numba engine not supporting duplicate index values"
        )
        request.node.add_marker(mark)
    df = DataFrame({"a": [0, 1, 2], "b": [1, 2, 3]})
    result = df[["a", "a"]].apply(
        lambda x: x.iloc[0] + x.iloc[1], axis=1, engine=engine
    )
    expected = Series([0, 2, 4])
    tm.assert_series_equal(result, expected)

