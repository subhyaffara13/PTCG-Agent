
def test_merge_series(on, left_on, right_on, left_index, right_index, nm):
    # GH 21220
    a = DataFrame(
        {"A": [1, 2, 3, 4]},
        index=MultiIndex.from_product([["a", "b"], [0, 1]], names=["outer", "inner"]),
    )
    b = Series(
        [1, 2, 3, 4],
        index=MultiIndex.from_product([["a", "b"], [1, 2]], names=["outer", "inner"]),
        name=nm,
    )
    expected = DataFrame(
        {"A": [2, 4], "B": [1, 3]},
        index=MultiIndex.from_product([["a", "b"], [1]], names=["outer", "inner"]),
    )
    if nm is not None:
        result = merge(
            a,
            b,
            on=on,
            left_on=left_on,
            right_on=right_on,
            left_index=left_index,
            right_index=right_index,
        )
        tm.assert_frame_equal(result, expected)
    else:
        msg = "Cannot merge a Series without a name"
        with pytest.raises(ValueError, match=msg):
            result = merge(
                a,
                b,
                on=on,
                left_on=left_on,
                right_on=right_on,
                left_index=left_index,
                right_index=right_index,
            )

