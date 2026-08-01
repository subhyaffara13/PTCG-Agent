
def test_apply_numeric_coercion_when_datetime_getitem():
    # GH 15421
    df = DataFrame(
        {"A": [10, 20, 30], "B": ["foo", "3", "4"], "T": [pd.Timestamp("12:31:22")] * 3}
    )

    def get_B(g):
        return g.iloc[0][["B"]]

    result = df.groupby("A").apply(get_B)["B"]
    expected = df.B
    expected.index = df.A
    tm.assert_series_equal(result, expected)

