
def test_keys_illegal_include_keyword_value(temp_hdfstore):
    with pytest.raises(
        ValueError,
        match="`include` should be either 'pandas' or 'native' but is 'illegal'",
    ):
        temp_hdfstore.keys(include="illegal")

