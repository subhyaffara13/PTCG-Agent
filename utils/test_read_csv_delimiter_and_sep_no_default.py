
def test_read_csv_delimiter_and_sep_no_default(all_parsers):
    # GH#39823
    f = StringIO("a,b\n1,2")
    parser = all_parsers
    msg = "Specified a sep and a delimiter; you can only specify one."
    with pytest.raises(ValueError, match=msg):
        parser.read_csv(f, sep=" ", delimiter=".")

