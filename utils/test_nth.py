
def test_nth():
    assert nth(2, 'ABCDE') == 'C'
    assert nth(2, iter('ABCDE')) == 'C'
    assert nth(1, (3, 2, 1)) == 2
    assert nth(0, {'foo': 'bar'}) == 'foo'
    assert raises(StopIteration, lambda: nth(10, {10: 'foo'}))
    assert nth(-2, 'ABCDE') == 'D'
    assert raises(ValueError, lambda: nth(-2, iter('ABCDE')))


def test_nth():
    df = DataFrame([[1, np.nan], [1, 4], [5, 6]], columns=["A", "B"])
    gb = df.groupby("A")

    tm.assert_frame_equal(gb.nth(0), df.iloc[[0, 2]])
    tm.assert_frame_equal(gb.nth(1), df.iloc[[1]])
    tm.assert_frame_equal(gb.nth(2), df.loc[[]])
    tm.assert_frame_equal(gb.nth(-1), df.iloc[[1, 2]])
    tm.assert_frame_equal(gb.nth(-2), df.iloc[[0]])
    tm.assert_frame_equal(gb.nth(-3), df.loc[[]])
    tm.assert_series_equal(gb.B.nth(0), df.B.iloc[[0, 2]])
    tm.assert_series_equal(gb.B.nth(1), df.B.iloc[[1]])
    tm.assert_frame_equal(gb[["B"]].nth(0), df[["B"]].iloc[[0, 2]])

    tm.assert_frame_equal(gb.nth(0, dropna="any"), df.iloc[[1, 2]])
    tm.assert_frame_equal(gb.nth(-1, dropna="any"), df.iloc[[1, 2]])

    tm.assert_frame_equal(gb.nth(7, dropna="any"), df.iloc[:0])
    tm.assert_frame_equal(gb.nth(2, dropna="any"), df.iloc[:0])

