
def test_offset_deprecated_error():
    with pytest.raises(ValueError, match="Did you mean h"):
        date_range("2012-01-01", periods=3, freq="H")

