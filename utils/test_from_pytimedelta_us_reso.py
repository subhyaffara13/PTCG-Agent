
def test_from_pytimedelta_us_reso():
    # pytimedelta has microsecond resolution, so Timedelta(pytd) inherits that
    td = timedelta(days=4, minutes=3)
    result = Timedelta(td)
    assert result.to_pytimedelta() == td
    assert result._creso == NpyDatetimeUnit.NPY_FR_us.value

