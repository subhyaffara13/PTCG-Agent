import math


def test_map_callable(datetime_series, engine):  # noqa: F811
    with np.errstate(all="ignore"):
        tm.assert_series_equal(
            datetime_series.map(np.sqrt, engine=engine), np.sqrt(datetime_series)
        )

    # map function element-wise
    tm.assert_series_equal(
        datetime_series.map(math.exp, engine=engine), np.exp(datetime_series)
    )

    # empty series
    s = Series(dtype=object, name="foo", index=Index([], name="bar"))
    rs = s.map(lambda x: x, engine=engine)
    tm.assert_series_equal(s, rs)

    # check all metadata (GH 9322)
    assert s is not rs
    assert s.index is rs.index
    assert s.dtype == rs.dtype
    assert s.name == rs.name

    # index but no data
    s = Series(index=[1, 2, 3], dtype=np.float64)
    rs = s.map(lambda x: x, engine=engine)
    tm.assert_series_equal(s, rs)

