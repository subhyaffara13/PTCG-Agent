
def test_where_duplicate_axes_mixed_dtypes():
    # GH 25399, verify manually masking is not affected anymore by dtype of column for
    # duplicate axes.
    result = DataFrame(data=[[0, np.nan]], columns=Index(["A", "A"]))
    index, columns = result.axes
    mask = DataFrame(data=[[True, True]], columns=columns, index=index)
    a = result.astype(object).where(mask)
    b = result.astype("f8").where(mask)
    c = result.T.where(mask.T).T
    d = result.where(mask)  # used to fail with "cannot reindex from a duplicate axis"
    tm.assert_frame_equal(a.astype("f8"), b.astype("f8"))
    tm.assert_frame_equal(b.astype("f8"), c.astype("f8"))
    tm.assert_frame_equal(c.astype("f8"), d.astype("f8"))

