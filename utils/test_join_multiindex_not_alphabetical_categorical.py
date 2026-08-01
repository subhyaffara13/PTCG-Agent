
def test_join_multiindex_not_alphabetical_categorical(categories, values):
    # GH#38502
    left = DataFrame(
        {
            "first": ["A", "A"],
            "second": Categorical(categories, categories=categories),
            "value": [1, 2],
        }
    ).set_index(["first", "second"])
    right = DataFrame(
        {
            "first": ["A", "A", "B"],
            "second": Categorical(values, categories=categories),
            "value": [3, 4, 5],
        }
    ).set_index(["first", "second"])
    result = left.join(right, lsuffix="_left", rsuffix="_right")

    expected = DataFrame(
        {
            "first": ["A", "A"],
            "second": Categorical(categories, categories=categories),
            "value_left": [1, 2],
            "value_right": [3, 4],
        }
    ).set_index(["first", "second"])
    tm.assert_frame_equal(result, expected)

