
def test_result_type_series_result_other_index(int_frame_const_col, engine, request):
    # result_type should be consistent no matter which
    # path we take in the code

    if engine == "numba":
        mark = pytest.mark.xfail(
            reason="no support in numba Series constructor for list of columns"
        )
        request.node.add_marker(mark)
    df = int_frame_const_col
    # series result with other index
    columns = ["other", "col", "names"]
    result = df.apply(lambda x: Series([1, 2, 3], index=columns), axis=1, engine=engine)
    expected = df.copy()
    expected.columns = columns
    tm.assert_frame_equal(result, expected)

