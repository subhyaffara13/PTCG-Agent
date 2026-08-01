
def test_multi_index_no_level_names_implicit(all_parsers):
    parser = all_parsers
    data = """A,B,C,D
foo,one,2,3,4,5
foo,two,7,8,9,10
foo,three,12,13,14,15
bar,one,12,13,14,15
bar,two,12,13,14,15
"""

    result = parser.read_csv(StringIO(data))
    expected = DataFrame(
        [
            [2, 3, 4, 5],
            [7, 8, 9, 10],
            [12, 13, 14, 15],
            [12, 13, 14, 15],
            [12, 13, 14, 15],
        ],
        columns=["A", "B", "C", "D"],
        index=MultiIndex.from_tuples(
            [
                ("foo", "one"),
                ("foo", "two"),
                ("foo", "three"),
                ("bar", "one"),
                ("bar", "two"),
            ]
        ),
    )
    tm.assert_frame_equal(result, expected)

