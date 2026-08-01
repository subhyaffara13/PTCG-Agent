
def test_transform_select_columns(df):
    f = lambda x: x.mean()
    result = df.groupby("A")[["C", "D"]].transform(f)

    selection = df[["C", "D"]]
    expected = selection.groupby(df["A"]).transform(f)

    tm.assert_frame_equal(result, expected)

