
def test_transform_dictlike_mixed():
    # GH 40018 - mix of lists and non-lists in values of a dictionary
    df = DataFrame({"a": [1, 2], "b": [1, 4], "c": [1, 4]})
    result = df.transform({"b": ["sqrt", "abs"], "c": "sqrt"})
    expected = DataFrame(
        [[1.0, 1, 1.0], [2.0, 4, 2.0]],
        columns=MultiIndex([("b", "c"), ("sqrt", "abs")], [(0, 0, 1), (0, 1, 0)]),
    )
    tm.assert_frame_equal(result, expected)


def test_transform_dictlike_mixed():
    # GH 40018 - mix of lists and non-lists in values of a dictionary
    df = Series([1, 4])
    result = df.transform({"b": ["sqrt", "abs"], "c": "sqrt"})
    expected = DataFrame(
        [[1.0, 1, 1.0], [2.0, 4, 2.0]],
        columns=MultiIndex([("b", "c"), ("sqrt", "abs")], [(0, 0, 1), (0, 1, 0)]),
    )
    tm.assert_frame_equal(result, expected)

