
def test_result_type_broadcast(int_frame_const_col, request, engine):
    # result_type should be consistent no matter which
    # path we take in the code
    if engine == "numba":
        mark = pytest.mark.xfail(reason="numba engine doesn't support list return")
        request.node.add_marker(mark)
    df = int_frame_const_col
    if engine is MockEngineDecorator:
        with pytest.raises(
            NotImplementedError,
            match="result_type='broadcast' only implemented for the default engine",
        ):
            df.apply(
                lambda x: [1, 2, 3], axis=1, result_type="broadcast", engine=engine
            )
    else:
        # broadcast result
        result = df.apply(
            lambda x: [1, 2, 3], axis=1, result_type="broadcast", engine=engine
        )
        expected = df.copy()
        tm.assert_frame_equal(result, expected)

