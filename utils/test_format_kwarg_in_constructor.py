
def test_format_kwarg_in_constructor(temp_h5_path):
    # GH 13291

    msg = "format is not a defined argument for HDFStore"

    with pytest.raises(ValueError, match=msg):
        HDFStore(temp_h5_path, format="table")

