
def test_str_nan_dropped(all_parsers):
    # see gh-21131
    parser = all_parsers

    data = """File: small.csv,,
10010010233,0123,654
foo,,bar
01001000155,4530,898"""

    result = parser.read_csv(
        StringIO(data),
        header=None,
        names=["col1", "col2", "col3"],
        dtype={"col1": str, "col2": str, "col3": str},
    ).dropna()

    expected = DataFrame(
        {
            "col1": ["10010010233", "01001000155"],
            "col2": ["0123", "4530"],
            "col3": ["654", "898"],
        },
        index=[1, 3],
    )

    tm.assert_frame_equal(result, expected)

