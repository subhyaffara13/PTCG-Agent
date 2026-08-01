
def test_merge_asof_non_numerical_dtype_object():
    # GH#29130
    left = pd.DataFrame({"a": ["12", "13", "15"], "left_val1": ["a", "b", "c"]})
    right = pd.DataFrame({"a": ["a", "b", "c"], "left_val": ["d", "e", "f"]})
    with pytest.raises(
        MergeError,
        match=r"Incompatible merge dtype, .*, both sides must have numeric dtype",
    ):
        merge_asof(
            left,
            right,
            left_on="left_val1",
            right_on="a",
            left_by="a",
            right_by="left_val",
        )

