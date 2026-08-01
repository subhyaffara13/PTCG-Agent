
def test_multi_index_blank_df(all_parsers, data, columns, header, round_trip):
    # see gh-14545
    parser = all_parsers
    expected = DataFrame(columns=columns)
    data = expected.to_csv(index=False) if round_trip else data

    result = parser.read_csv(StringIO(data), header=header)
    tm.assert_frame_equal(result, expected)

