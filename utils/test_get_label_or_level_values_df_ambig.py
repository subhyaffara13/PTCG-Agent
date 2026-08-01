
def test_get_label_or_level_values_df_ambig(df_ambig, axis):
    axis = df_ambig._get_axis_number(axis)
    # Transpose frame if axis == 1
    if axis == 1:
        df_ambig = df_ambig.T

    # df has an on-axis level named L2, and it is not ambiguous.
    assert_level_values(df_ambig, ["L2"], axis=axis)

    # df has an off-axis label named L3, and it is not ambiguous.
    assert_label_values(df_ambig, ["L3"], axis=axis)

