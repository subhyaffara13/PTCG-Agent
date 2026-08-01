
def test_unstack_mixed_type_name_in_multiindex(
    unstack_idx, expected_values, expected_index, expected_columns
):
    # GH 19966
    idx = MultiIndex.from_product(
        [["a", "b"], [1, 2], [3, 4]], names=[("A", "a"), "B", "C"]
    )
    ser = Series(1, index=idx)
    result = ser.unstack(unstack_idx)

    expected = DataFrame(
        expected_values, columns=expected_columns, index=expected_index
    )
    tm.assert_frame_equal(result, expected)

