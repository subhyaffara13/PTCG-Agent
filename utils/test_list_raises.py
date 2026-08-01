
def test_list_raises(string_series):
    with pytest.raises(TypeError, match="'list' object is not callable"):
        string_series.map([lambda x: x])

