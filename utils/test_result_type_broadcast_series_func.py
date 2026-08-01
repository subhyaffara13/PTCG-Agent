
def test_result_type_broadcast_series_func(int_frame_const_col, engine, request):
    # result_type should be consistent no matter which
    # path we take in the code
    if engine == "numba":
        mark = pytest.mark.xfail(
            reason="numba Series constructor only support ndarrays not list data"
        )
        request.node.add_marker(mark)
    df = int_frame_const_col
    columns = ["other", "col", "names"]

    if engine is MockEngineDecorator:
        with pytest.raises(
            NotImplementedError,
            match="result_type='broadcast' only implemented for the default engine",
        ):
            df.apply(
                lambda x: Series([1, 2, 3], index=columns),
                axis=1,
                result_type="broadcast",
                engine=engine,
            )
    else:
        result = df.apply(
            lambda x: Series([1, 2, 3], index=columns),
            axis=1,
            result_type="broadcast",
            engine=engine,
        )
        expected = df.copy()
        tm.assert_frame_equal(result, expected)

