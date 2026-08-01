
def test_timestamp_constructor_na_value(na_value):
    # GH45481
    result = Timestamp(na_value)
    expected = NaT
    assert result is expected

