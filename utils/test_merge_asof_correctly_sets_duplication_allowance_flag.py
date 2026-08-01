
def test_merge_asof_correctly_sets_duplication_allowance_flag(
    allow_on_left: bool,
    allow_on_right: bool,
):
    left = pd.DataFrame({"test": [1]}).set_flags(allows_duplicate_labels=allow_on_left)
    right = pd.DataFrame({"test": [1]}).set_flags(
        allows_duplicate_labels=allow_on_right,
    )

    result = pd.merge_asof(left, right)

    expected_duplication_allowance = allow_on_left and allow_on_right
    assert result.flags.allows_duplicate_labels == expected_duplication_allowance

