
def test_merge_does_not_propagate_metadata_if_one_input_has_no_metadata(
    left_has_metadata: bool,
    right_has_metadata: bool,
    expected: dict,
):
    left = pd.DataFrame({"test": [1]})
    right = pd.DataFrame({"test": [1]})

    if left_has_metadata:
        left.attrs = {"a": [1, 2]}
    else:
        left.attrs = {}

    if right_has_metadata:
        right.attrs = {"a": [1, 2]}
    else:
        right.attrs = {}

    result = left.merge(right, how="inner", on="test")

    assert result.attrs == expected

