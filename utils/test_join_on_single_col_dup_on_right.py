
def test_join_on_single_col_dup_on_right(left_no_dup, right_w_dups, dtype):
    # GH 46622
    # Dups on right allowed by one_to_many constraint
    if dtype == "string[pyarrow]":
        pytest.importorskip("pyarrow")
    left_no_dup = left_no_dup.astype(dtype)
    right_w_dups.index = right_w_dups.index.astype(dtype)
    left_no_dup.join(
        right_w_dups,
        on="a",
        validate="one_to_many",
    )

    # Dups on right not allowed by one_to_one constraint
    msg = "Merge keys are not unique in right dataset; not a one-to-one merge"
    with pytest.raises(MergeError, match=msg):
        left_no_dup.join(
            right_w_dups,
            on="a",
            validate="one_to_one",
        )

