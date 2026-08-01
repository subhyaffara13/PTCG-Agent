
def test_constructor_from_dict():
    # https://github.com/pandas-dev/pandas/issues/52445
    result = SubclassedSeries({"a": 1, "b": 2, "c": 3})
    assert isinstance(result, SubclassedSeries)

