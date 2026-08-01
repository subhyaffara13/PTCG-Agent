
def test_rolling_decreasing_indices(method):
    """
    Make sure that decreasing indices give the same results as increasing indices.

    GH 36933
    """
    df = DataFrame({"values": np.arange(-15, 10) ** 2})
    df_reverse = DataFrame({"values": df["values"][::-1]}, index=df.index[::-1])

    increasing = getattr(df.rolling(window=5), method)()
    decreasing = getattr(df_reverse.rolling(window=5), method)()

    tm.assert_almost_equal(
        decreasing.values[::-1][:-4], increasing.values[4:], atol=1e-12
    )

