
def df_table():
    return DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": ["a", "b", "c", "c"],
            "C": pd.date_range("2016-01-01", freq="D", periods=4),
            "D": pd.timedelta_range("1h", periods=4, freq="min"),
            "E": pd.Series(pd.Categorical(["a", "b", "c", "c"])),
            "F": pd.Series(pd.Categorical(["a", "b", "c", "c"], ordered=True)),
            "G": [1.0, 2.0, 3, 4.0],
            "H": pd.date_range("2016-01-01", freq="D", periods=4, tz="US/Central"),
        },
        index=pd.Index(range(4), name="idx"),
    )

