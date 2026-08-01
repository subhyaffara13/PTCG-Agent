
def test_join_empty(left_empty, how, exp):
    left = DataFrame({"A": [2, 1], "B": [3, 4]}, dtype="int64").set_index("A")
    right = DataFrame({"A": [1], "C": [5]}, dtype="int64").set_index("A")

    if left_empty:
        left = left.head(0)
    else:
        right = right.head(0)

    result = left.join(right, how=how)

    if exp == "left":
        expected = DataFrame({"A": [2, 1], "B": [3, 4], "C": [np.nan, np.nan]})
        expected = expected.set_index("A")
    elif exp == "right":
        expected = DataFrame({"B": [np.nan], "A": [1], "C": [5]})
        expected = expected.set_index("A")
    elif exp == "empty":
        expected = DataFrame(columns=["B", "C"], dtype="int64")
        if how != "cross":
            expected = expected.rename_axis("A")
    if how == "outer":
        expected = expected.sort_index()

    tm.assert_frame_equal(result, expected)

