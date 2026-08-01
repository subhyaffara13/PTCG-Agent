
def df_schema():
    return DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": ["a", "b", "c", "c"],
            "C": pd.date_range("2016-01-01", freq="D", periods=4),
            "D": pd.timedelta_range("1h", periods=4, freq="min"),
        },
        index=pd.Index(range(4), name="idx"),
    )

