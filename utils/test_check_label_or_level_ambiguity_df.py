
def test_check_label_or_level_ambiguity_df(df_ambig, axis):
    axis = df_ambig._get_axis_number(axis)
    # Transpose frame if axis == 1
    if axis == 1:
        df_ambig = df_ambig.T
        msg = "'L1' is both a column level and an index label"

    else:
        msg = "'L1' is both an index level and a column label"
    # df_ambig has both an on-axis level and off-axis label named L1
    # Therefore, L1 is ambiguous.
    with pytest.raises(ValueError, match=msg):
        df_ambig._check_label_or_level_ambiguity("L1", axis=axis)

    # df_ambig has an on-axis level named L2,, and it is not ambiguous.
    df_ambig._check_label_or_level_ambiguity("L2", axis=axis)

    # df_ambig has an off-axis label named L3, and it is not ambiguous
    assert not df_ambig._check_label_or_level_ambiguity("L3", axis=axis)

