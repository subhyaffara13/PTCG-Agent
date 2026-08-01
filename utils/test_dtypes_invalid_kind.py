
def test_dtypes_invalid_kind():
    with pytest.raises(ValueError, match="unsupported kind"):
        info.dtypes(kind="invalid")

