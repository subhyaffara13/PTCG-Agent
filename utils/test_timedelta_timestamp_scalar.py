
def test_timedelta_timestamp_scalar(scalar):
    # GH#59944
    result = to_numeric(scalar)
    expected = to_numeric(Series(scalar))[0]
    assert result == expected

