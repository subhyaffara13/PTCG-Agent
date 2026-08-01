
def test_merge_correctly_sets_duplication_allowance_flag(
    how: MergeHow,
    allow_on_left: bool,
    allow_on_right: bool,
):
    left = pd.DataFrame({"test": [1]}).set_flags(allows_duplicate_labels=allow_on_left)
    right = pd.DataFrame({"test": [1]}).set_flags(
        allows_duplicate_labels=allow_on_right,
    )

    if not how == "cross":
        result = left.merge(right, how=how, on="test")
    else:
        result = left.merge(right, how=how)

    expected_duplication_allowance = allow_on_left and allow_on_right
    assert result.flags.allows_duplicate_labels == expected_duplication_allowance

