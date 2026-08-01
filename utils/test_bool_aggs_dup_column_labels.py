
def test_bool_aggs_dup_column_labels(all_boolean_reductions):
    # GH#21668
    df = DataFrame([[True, True]], columns=["a", "a"])
    grp_by = df.groupby([0])
    result = getattr(grp_by, all_boolean_reductions)()

    expected = df.set_axis(np.array([0]))
    tm.assert_frame_equal(result, expected)

