
def multiindex_year_month_day_dataframe_random_data():
    """
    DataFrame with 3 level MultiIndex (year, month, day) covering
    first 100 business days from 2000-01-01 with random data
    """
    tdf = DataFrame(
        np.random.default_rng(2).standard_normal((100, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=100, freq="B"),
    )
    ymd = tdf.groupby([lambda x: x.year, lambda x: x.month, lambda x: x.day]).sum()
    # use int64 Index, to make sure things work
    ymd.index = ymd.index.set_levels([lev.astype("i8") for lev in ymd.index.levels])
    ymd.index.set_names(["year", "month", "day"], inplace=True)
    return ymd

