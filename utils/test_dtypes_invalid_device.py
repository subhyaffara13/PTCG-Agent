
def test_dtypes_invalid_device():
    with pytest.raises(ValueError, match="Device not understood"):
        info.dtypes(device="gpu")

