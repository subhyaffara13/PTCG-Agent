
def test_skip_whitespace(c_parser_only, float_precision):
    DATA = """id\tnum\t
1\t1.2 \t
1\t 2.1\t
2\t 1\t
2\t 1.2 \t
"""
    df = c_parser_only.read_csv(
        StringIO(DATA),
        float_precision=float_precision,
        sep="\t",
        header=0,
        dtype={1: np.float64},
    )
    tm.assert_series_equal(df.iloc[:, 1], pd.Series([1.2, 2.1, 1.0, 1.2], name="num"))

