
def test_pandas_minimal_plot(pd):
    # smoke test that series and index objects do not warn
    for x in [pd.Series([1, 2], dtype="float64"),
              pd.Series([1, 2], dtype="Float64")]:
        plt.plot(x, x)
        plt.plot(x.index, x)
        plt.plot(x)
        plt.plot(x.index)
    df = pd.DataFrame({'col': [1, 2, 3]})
    plt.plot(df)
    plt.plot(df, df)

