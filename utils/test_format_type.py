
def test_format_type(temp_hdfstore):
    df = DataFrame({"A": [1, 2]})
    temp_hdfstore.put("a", df, format="fixed")
    temp_hdfstore.put("b", df, format="table")

    assert temp_hdfstore.get_storer("a").format_type == "fixed"
    assert temp_hdfstore.get_storer("b").format_type == "table"

