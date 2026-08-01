
def test_is_level_or_label_reference_df_simple(df_levels, axis):
    axis = df_levels._get_axis_number(axis)
    # Compute expected labels and levels
    expected_labels, expected_levels = get_labels_levels(df_levels)

    # Transpose frame if axis == 1
    if axis == 1:
        df_levels = df_levels.T

    # Perform checks
    assert_level_reference(df_levels, expected_levels, axis=axis)
    assert_label_reference(df_levels, expected_labels, axis=axis)

