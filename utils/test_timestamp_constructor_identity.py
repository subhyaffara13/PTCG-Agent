
def test_timestamp_constructor_identity():
    # Test for #30543
    expected = Timestamp("2017-01-01T12")
    result = Timestamp(expected)
    assert result is expected

