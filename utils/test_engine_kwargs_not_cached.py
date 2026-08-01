
def test_engine_kwargs_not_cached():
    # If the user passes a different set of engine_kwargs don't return the same
    # jitted function
    pytest.importorskip("numba")
    nogil = True
    parallel = False
    nopython = True

    def func_kwargs(values, index):
        return nogil + parallel + nopython

    engine_kwargs = {"nopython": nopython, "nogil": nogil, "parallel": parallel}
    df = DataFrame({"value": [0, 0, 0]})
    result = df.groupby(level=0).aggregate(
        func_kwargs, engine="numba", engine_kwargs=engine_kwargs
    )
    expected = DataFrame({"value": [2.0, 2.0, 2.0]})
    tm.assert_frame_equal(result, expected)

    nogil = False
    engine_kwargs = {"nopython": nopython, "nogil": nogil, "parallel": parallel}
    result = df.groupby(level=0).aggregate(
        func_kwargs, engine="numba", engine_kwargs=engine_kwargs
    )
    expected = DataFrame({"value": [1.0, 1.0, 1.0]})
    tm.assert_frame_equal(result, expected)


def test_engine_kwargs_not_cached():
    # If the user passes a different set of engine_kwargs don't return the same
    # jitted function
    pytest.importorskip("numba")
    nogil = True
    parallel = False
    nopython = True

    def func_kwargs(values, index):
        return nogil + parallel + nopython

    engine_kwargs = {"nopython": nopython, "nogil": nogil, "parallel": parallel}
    df = DataFrame({"value": [0, 0, 0]})
    result = df.groupby(level=0).transform(
        func_kwargs, engine="numba", engine_kwargs=engine_kwargs
    )
    expected = DataFrame({"value": [2.0, 2.0, 2.0]})
    tm.assert_frame_equal(result, expected)

    nogil = False
    engine_kwargs = {"nopython": nopython, "nogil": nogil, "parallel": parallel}
    result = df.groupby(level=0).transform(
        func_kwargs, engine="numba", engine_kwargs=engine_kwargs
    )
    expected = DataFrame({"value": [1.0, 1.0, 1.0]})
    tm.assert_frame_equal(result, expected)

