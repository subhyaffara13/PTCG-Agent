
def test_merge_on_left_categoricalindex():
    # GH#48464 don't raise when left_on is a CategoricalIndex
    ci = CategoricalIndex(range(3))

    right = DataFrame({"A": ci, "B": range(3)})
    left = DataFrame({"C": range(3, 6)})

    res = merge(left, right, left_on=ci, right_on="A")
    expected = merge(left, right, left_on=ci._data, right_on="A")
    tm.assert_frame_equal(res, expected)

