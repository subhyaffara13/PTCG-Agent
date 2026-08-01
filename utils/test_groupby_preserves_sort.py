
def test_groupby_preserves_sort(sort_column, group_column):
    # Test to ensure that groupby always preserves sort order of original
    # object. Issue #8588 and #9651

    df = DataFrame(
        {
            "int_groups": [3, 1, 0, 1, 0, 3, 3, 3],
            "string_groups": ["z", "a", "z", "a", "a", "g", "g", "g"],
            "ints": [8, 7, 4, 5, 2, 9, 1, 1],
            "floats": [2.3, 5.3, 6.2, -2.4, 2.2, 1.1, 1.1, 5],
            "strings": ["z", "d", "a", "e", "word", "word2", "42", "47"],
        }
    )

    # Try sorting on different types and with different group types

    df = df.sort_values(by=sort_column)
    g = df.groupby(group_column)

    def test_sort(x):
        tm.assert_frame_equal(x, x.sort_values(by=sort_column))

    g.apply(test_sort)

