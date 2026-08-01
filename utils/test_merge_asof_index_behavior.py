
def test_merge_asof_index_behavior(kwargs):
    # GH 33463
    index = Index([1, 5, 10], name="test")
    left = pd.DataFrame({"left": ["a", "b", "c"], "left_time": [1, 4, 10]}, index=index)
    right = pd.DataFrame({"right": [1, 2, 3, 6, 7]}, index=[1, 2, 3, 6, 7])
    result = merge_asof(left, right, **kwargs)

    expected = pd.DataFrame(
        {"left": ["a", "b", "c"], "left_time": [1, 4, 10], "right": [1, 3, 7]},
        index=index,
    )
    tm.assert_frame_equal(result, expected)

