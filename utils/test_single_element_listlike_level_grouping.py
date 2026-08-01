
def test_single_element_listlike_level_grouping(level_arg, multiindex):
    # GH 51583
    df = DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]}, index=["x", "y"])
    if multiindex:
        df = df.set_index(["a", "b"])
    result = [key for key, _ in df.groupby(level=level_arg)]
    expected = [(1,), (2,)] if multiindex else [("x",), ("y",)]
    assert result == expected

