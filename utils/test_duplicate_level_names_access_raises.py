
def test_duplicate_level_names_access_raises(idx):
    # GH19029
    idx.names = ["foo", "foo"]
    with pytest.raises(ValueError, match="name foo occurs multiple times"):
        idx._get_level_number("foo")

