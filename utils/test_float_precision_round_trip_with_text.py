
def test_float_precision_round_trip_with_text(c_parser_only):
    # see gh-15140
    parser = c_parser_only
    df = parser.read_csv(StringIO("a"), header=None, float_precision="round_trip")
    tm.assert_frame_equal(df, DataFrame({0: ["a"]}))

