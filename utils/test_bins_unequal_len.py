
def test_bins_unequal_len():
    # GH3011
    series = Series([np.nan, np.nan, 1, 1, 2, 2, 3, 3, 4, 4])
    bins = pd.cut(series.dropna().values, 4)

    # len(bins) != len(series) here
    with pytest.raises(ValueError, match="Grouper and axis must be same length"):
        series.groupby(bins).mean()

