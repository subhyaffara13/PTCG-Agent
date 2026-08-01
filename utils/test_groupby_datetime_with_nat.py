
def test_groupby_datetime_with_nat():
    # GH##35202
    df = DataFrame(
        {
            "a": [
                to_datetime("2019-02-12"),
                to_datetime("2019-02-12"),
                to_datetime("2019-02-13"),
                pd.NaT,
            ],
            "b": [1, 2, 3, 4],
        }
    )
    grouped = df.groupby("a", dropna=False)
    result = len(grouped)
    assert result == 3

