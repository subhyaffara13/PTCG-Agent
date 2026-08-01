
def test_merge_asof_raise_for_duplicate_columns():
    # GH#50102
    left = pd.DataFrame([[1, 2, "a"]], columns=["a", "a", "left_val"])
    right = pd.DataFrame([[1, 1, 1]], columns=["a", "a", "right_val"])

    with pytest.raises(ValueError, match="column label 'a'"):
        merge_asof(left, right, on="a")

    with pytest.raises(ValueError, match="column label 'a'"):
        merge_asof(left, right, left_on="a", right_on="right_val")

    with pytest.raises(ValueError, match="column label 'a'"):
        merge_asof(left, right, left_on="left_val", right_on="a")

