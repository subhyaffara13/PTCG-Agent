
def test_ms_to_timestamp_error_message():
    # https://github.com/pandas-dev/pandas/issues/58974#issuecomment-2164265446
    ix = period_range("2000", periods=3, freq="M")
    with pytest.raises(ValueError, match="for Period, please use 'M' instead of 'MS'"):
        ix.to_timestamp("MS")

