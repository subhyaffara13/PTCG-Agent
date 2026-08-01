
def test_merge_propagates_metadata_from_equal_input_metadata():
    metadata = {"a": [1, 2]}
    left = pd.DataFrame({"test": [1]})
    left.attrs = metadata
    right = pd.DataFrame({"test": [1]})
    right.attrs = deepcopy(metadata)

    result = left.merge(right, how="inner", on="test")

    assert result.attrs == metadata

    # Verify that merge deep-copies the attr dictionary.
    assert result.attrs is not left.attrs
    assert result.attrs is not right.attrs
    assert result.attrs["a"] is not left.attrs["a"]
    assert result.attrs["a"] is not right.attrs["a"]

