
def test_ea_int_avoid_overflow(all_parsers):
    # GH#32134
    parser = all_parsers
    data = """a,b
1,1
,1
1582218195625938945,1
"""
    result = parser.read_csv(StringIO(data), dtype={"a": "Int64"})
    expected = DataFrame(
        {
            "a": IntegerArray(
                np.array([1, 1, 1582218195625938945]), np.array([False, True, False])
            ),
            "b": 1,
        }
    )
    tm.assert_frame_equal(result, expected)

