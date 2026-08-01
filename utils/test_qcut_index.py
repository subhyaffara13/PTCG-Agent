
def test_qcut_index():
    result = qcut([0, 2], 2)
    intervals = [Interval(-0.001, 1), Interval(1, 2)]

    expected = Categorical(intervals, ordered=True)
    tm.assert_categorical_equal(result, expected)

