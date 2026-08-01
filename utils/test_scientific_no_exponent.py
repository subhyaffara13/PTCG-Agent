
def test_scientific_no_exponent(all_parsers_all_precisions):
    # see gh-12215
    df = DataFrame.from_dict({"w": ["2e"], "x": ["3E"], "y": ["42e"], "z": ["632E"]})
    data = df.to_csv(index=False)
    parser, precision = all_parsers_all_precisions

    df_roundtrip = parser.read_csv(StringIO(data), float_precision=precision)
    tm.assert_frame_equal(df_roundtrip, df)

