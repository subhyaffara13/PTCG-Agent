
def test_to_datetime_mixed_not_necessarily_iso8601_raise():
    # https://github.com/pandas-dev/pandas/issues/50411
    with pytest.raises(ValueError, match="Time data 01-01-2000 is not ISO8601 format"):
        to_datetime(["2020-01-01", "01-01-2000"], format="ISO8601")

