
def test_check_nopython_kwargs():
    pytest.importorskip("numba")

    def incorrect_function(values, index, *, a):
        return sum(values) * 2.7 + a

    def correct_function(values, index, a):
        return sum(values) * 2.7 + a

    data = DataFrame(
        {"key": ["a", "a", "b", "b", "a"], "data": [1.0, 2.0, 3.0, 4.0, 5.0]},
        columns=["key", "data"],
    )
    expected = data.groupby("key").sum() * 2.7

    # py signature binding
    with pytest.raises(
        TypeError, match="missing a required (keyword-only argument|argument): 'a'"
    ):
        data.groupby("key").agg(incorrect_function, engine="numba", b=1)
    with pytest.raises(TypeError, match="missing a required argument: 'a'"):
        data.groupby("key").agg(correct_function, engine="numba", b=1)

    with pytest.raises(
        TypeError, match="missing a required (keyword-only argument|argument): 'a'"
    ):
        data.groupby("key")["data"].agg(incorrect_function, engine="numba", b=1)
    with pytest.raises(TypeError, match="missing a required argument: 'a'"):
        data.groupby("key")["data"].agg(correct_function, engine="numba", b=1)

    # numba signature check after binding
    with pytest.raises(NumbaUtilError, match="numba does not support"):
        data.groupby("key").agg(incorrect_function, engine="numba", a=1)
    actual = data.groupby("key").agg(correct_function, engine="numba", a=1)
    tm.assert_frame_equal(expected + 1, actual)

    with pytest.raises(NumbaUtilError, match="numba does not support"):
        data.groupby("key")["data"].agg(incorrect_function, engine="numba", a=1)
    actual = data.groupby("key")["data"].agg(correct_function, engine="numba", a=1)
    tm.assert_series_equal(expected["data"] + 1, actual)


def test_check_nopython_kwargs():
    pytest.importorskip("numba")

    def incorrect_function(values, index, *, a):
        return values + a

    def correct_function(values, index, a):
        return values + a

    data = DataFrame(
        {"key": ["a", "a", "b", "b", "a"], "data": [1.0, 2.0, 3.0, 4.0, 5.0]},
        columns=["key", "data"],
    )
    # py signature binding
    with pytest.raises(
        TypeError, match="missing a required (keyword-only argument|argument): 'a'"
    ):
        data.groupby("key").transform(incorrect_function, engine="numba", b=1)
    with pytest.raises(TypeError, match="missing a required argument: 'a'"):
        data.groupby("key").transform(correct_function, engine="numba", b=1)

    with pytest.raises(
        TypeError, match="missing a required (keyword-only argument|argument): 'a'"
    ):
        data.groupby("key")["data"].transform(incorrect_function, engine="numba", b=1)
    with pytest.raises(TypeError, match="missing a required argument: 'a'"):
        data.groupby("key")["data"].transform(correct_function, engine="numba", b=1)

    # numba signature check after binding
    with pytest.raises(NumbaUtilError, match="numba does not support"):
        data.groupby("key").transform(incorrect_function, engine="numba", a=1)
    actual = data.groupby("key").transform(correct_function, engine="numba", a=1)
    tm.assert_frame_equal(data[["data"]] + 1, actual)

    with pytest.raises(NumbaUtilError, match="numba does not support"):
        data.groupby("key")["data"].transform(incorrect_function, engine="numba", a=1)
    actual = data.groupby("key")["data"].transform(
        correct_function, engine="numba", a=1
    )
    tm.assert_series_equal(data["data"] + 1, actual)

