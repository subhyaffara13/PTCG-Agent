
def test_get_label_or_level_values_df_duplabels(df, axis):
    df = df.set_index(["L1"])
    df_duplabels = pd.concat([df, df["L2"]], axis=1)
    axis = df_duplabels._get_axis_number(axis)
    # Transpose frame if axis == 1
    if axis == 1:
        df_duplabels = df_duplabels.T

    # df has unambiguous level 'L1'
    assert_level_values(df_duplabels, ["L1"], axis=axis)

    # df has unique label 'L3'
    assert_label_values(df_duplabels, ["L3"], axis=axis)

    # df has duplicate labels 'L2'
    if axis == 0:
        expected_msg = "The column label 'L2' is not unique"
    else:
        expected_msg = "The index label 'L2' is not unique"

    with pytest.raises(ValueError, match=expected_msg):
        assert_label_values(df_duplabels, ["L2"], axis=axis)

