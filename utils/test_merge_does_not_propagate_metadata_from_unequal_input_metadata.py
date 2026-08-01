
def test_merge_does_not_propagate_metadata_from_unequal_input_metadata():
    left = pd.DataFrame({"test": [1]})
    left.attrs = {"a": 2}
    right = pd.DataFrame({"test": [1]})
    right.attrs = {"b": 3}

    result = left.merge(right, how="inner", on="test")

    assert result.attrs == {}

