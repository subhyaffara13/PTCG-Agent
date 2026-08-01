
def test_nat_parse(all_parsers, temp_file):
    # see gh-3062
    parser = all_parsers
    df = DataFrame(
        {
            "A": np.arange(10, dtype="float64"),
            "B": Timestamp("20010101"),
        }
    )
    df.iloc[3:6, :] = np.nan

    path = temp_file
    df.to_csv(path)

    result = parser.read_csv(path, index_col=0, parse_dates=["B"])
    tm.assert_frame_equal(result, df)

