
def test_read_csv_low_memory_no_rows_with_index(all_parsers):
    # see gh-21141
    parser = all_parsers

    if not parser.low_memory:
        pytest.skip("This is a low-memory specific test")

    data = """A,B,C
1,1,1,2
2,2,3,4
3,3,4,5
"""

    if parser.engine == "pyarrow":
        msg = "The 'nrows' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), low_memory=True, index_col=0, nrows=0)
        return

    result = parser.read_csv(StringIO(data), low_memory=True, index_col=0, nrows=0)
    expected = DataFrame(columns=["A", "B", "C"])
    tm.assert_frame_equal(result, expected)

