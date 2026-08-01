
def test_result_type_series_result(int_frame_const_col, engine, request):
    # result_type should be consistent no matter which
    # path we take in the code
    if engine == "numba":
        mark = pytest.mark.xfail(
            reason="numba Series constructor only support ndarrays not list data"
        )
        request.node.add_marker(mark)
    df = int_frame_const_col
    # series result
    result = df.apply(lambda x: Series([1, 2, 3], index=x.index), axis=1, engine=engine)
    expected = df.copy()
    tm.assert_frame_equal(result, expected)

