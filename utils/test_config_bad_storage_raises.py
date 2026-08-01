
def test_config_bad_storage_raises():
    msg = re.escape("Value must be one of python|pyarrow")
    with pytest.raises(ValueError, match=msg):
        pd.options.mode.string_storage = "foo"

