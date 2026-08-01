
def test_fails_on_no_datetime_index(index):
    name = type(index).__name__
    df = DataFrame({"a": range(len(index))}, index=index)

    msg = (
        "Only valid with DatetimeIndex, TimedeltaIndex "
        f"or PeriodIndex, but got an instance of '{name}'"
    )
    with pytest.raises(TypeError, match=msg):
        df.groupby(Grouper(freq="D"))

