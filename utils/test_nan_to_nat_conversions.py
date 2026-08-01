
def test_nan_to_nat_conversions():
    df = DataFrame(
        {"A": np.asarray(range(10), dtype="float64"), "B": Timestamp("20010101")}
    )
    df.iloc[3:6, :] = np.nan
    result = df.loc[4, "B"]
    assert result is pd.NaT

    s = df["B"].copy()
    s[8:9] = np.nan
    assert s[8] is pd.NaT

