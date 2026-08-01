
def test_missing_parse_dates_column_raises(
    all_parsers, names, usecols, parse_dates, missing_cols
):
    # gh-31251 column names provided in parse_dates could be missing.
    parser = all_parsers
    content = StringIO("date,time,val\n2020-01-31,04:20:32,32\n")
    msg = f"Missing column provided to 'parse_dates': '{missing_cols}'"

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(
            content, sep=",", names=names, usecols=usecols, parse_dates=parse_dates
        )

