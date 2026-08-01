
def test_invalid_kwargs_nopython():
    with pytest.raises(TypeError, match="got an unexpected keyword argument 'a'"):
        Series(range(1)).rolling(1).apply(
            lambda x: x, kwargs={"a": 1}, engine="numba", raw=True
        )
    with pytest.raises(
        NumbaUtilError, match="numba does not support keyword-only arguments"
    ):
        Series(range(1)).rolling(1).apply(
            lambda x, *, a: x, kwargs={"a": 1}, engine="numba", raw=True
        )

    tm.assert_series_equal(
        Series(range(1), dtype=float) + 1,
        Series(range(1))
        .rolling(1)
        .apply(lambda x, a: (x + a).sum(), kwargs={"a": 1}, engine="numba", raw=True),
    )

