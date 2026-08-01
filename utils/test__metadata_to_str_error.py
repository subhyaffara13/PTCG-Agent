
def test__metadata_to_str_error(value):
    with pytest.raises(ValueError, match="value must not contain the chars"):
        _metadata_to_str("Title", value)

