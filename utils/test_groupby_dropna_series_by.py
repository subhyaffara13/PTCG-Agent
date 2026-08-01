
def test_groupby_dropna_series_by(dropna, expected):
    ser = pd.Series(
        [390.0, 350.0, 30.0, 20.0],
        index=["Falcon", "Falcon", "Parrot", "Parrot"],
        name="Max Speed",
    )

    result = ser.groupby(["a", "b", "a", np.nan], dropna=dropna).mean()
    tm.assert_series_equal(result, expected)

