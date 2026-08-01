
def test_against_scalar_parametric(freq, dt, n):
    # https://github.com/pandas-dev/pandas/issues/49606
    freq = f"{n}{freq}"
    d = date_range(dt, periods=3, freq=freq)
    result = list(d.is_year_start)
    expected = [x.is_year_start for x in d]
    assert result == expected

