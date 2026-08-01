
def test_nullable_int_dtype(all_parsers, any_int_ea_dtype):
    # GH 25472
    parser = all_parsers
    dtype = any_int_ea_dtype

    data = """a,b,c
,3,5
1,,6
2,4,"""
    expected = DataFrame(
        {
            "a": pd.array([pd.NA, 1, 2], dtype=dtype),
            "b": pd.array([3, pd.NA, 4], dtype=dtype),
            "c": pd.array([5, 6, pd.NA], dtype=dtype),
        }
    )
    actual = parser.read_csv(StringIO(data), dtype=dtype)
    tm.assert_frame_equal(actual, expected)

