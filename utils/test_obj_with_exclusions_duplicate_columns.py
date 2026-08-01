
def test_obj_with_exclusions_duplicate_columns():
    # GH#50806
    df = DataFrame([[0, 1, 2, 3]])
    df.columns = [0, 1, 2, 0]
    gb = df.groupby(df[1])
    result = gb._obj_with_exclusions
    expected = df.take([0, 2, 3], axis=1)
    tm.assert_frame_equal(result, expected)

