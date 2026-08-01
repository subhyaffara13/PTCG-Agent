
def test_subsetting_columns_keeps_attrs(klass, attr, value):
    # GH 9959 - When subsetting columns, don't drop attributes
    df = DataFrame({"a": [1], "b": [2], "c": [3]})
    if attr != "axis":
        df = df.set_index("a")

    expected = df.groupby("a", **{attr: value})
    result = expected[["b"]] if klass is DataFrame else expected["b"]
    assert getattr(result, attr) == getattr(expected, attr)

