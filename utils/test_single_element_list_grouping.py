
def test_single_element_list_grouping(selection):
    # GH#42795, GH#53500
    df = DataFrame({"a": [1, 2], "b": [np.nan, 5], "c": [np.nan, 2]}, index=["x", "y"])
    grouped = df.groupby(["a"]) if selection is None else df.groupby(["a"])[selection]
    result = [key for key, _ in grouped]

    expected = [(1,), (2,)]
    assert result == expected

