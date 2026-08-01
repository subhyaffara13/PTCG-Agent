
def test_join_on_single_col_dup_on_both(left_w_dups, right_w_dups):
    # GH 46622
    # Dups on both allowed by many_to_many constraint
    left_w_dups.join(right_w_dups, on="a", validate="many_to_many")

    # Dups on both not allowed by many_to_one constraint
    msg = "Merge keys are not unique in right dataset; not a many-to-one merge"
    with pytest.raises(MergeError, match=msg):
        left_w_dups.join(
            right_w_dups,
            on="a",
            validate="many_to_one",
        )

    # Dups on both not allowed by one_to_many constraint
    msg = "Merge keys are not unique in left dataset; not a one-to-many merge"
    with pytest.raises(MergeError, match=msg):
        left_w_dups.join(
            right_w_dups,
            on="a",
            validate="one_to_many",
        )

