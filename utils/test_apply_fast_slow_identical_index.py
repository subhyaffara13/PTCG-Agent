
def test_apply_fast_slow_identical_index():
    # GH#44803
    df = DataFrame(
        {
            "name": ["Alice", "Bob", "Carl"],
            "age": [20, 21, 20],
        }
    ).set_index("name")

    grp_by_same_value = df.groupby(["age"], group_keys=False).apply(lambda group: group)
    grp_by_copy = df.groupby(["age"], group_keys=False).apply(
        lambda group: group.copy()
    )
    tm.assert_frame_equal(grp_by_same_value, grp_by_copy)

