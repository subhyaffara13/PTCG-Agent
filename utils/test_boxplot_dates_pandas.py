
def test_boxplot_dates_pandas(pd):
    # smoke test for boxplot and dates in pandas
    data = np.random.rand(5, 2)
    years = pd.date_range('1/1/2000',
                          periods=2, freq=pd.DateOffset(years=1)).year
    plt.figure()
    plt.boxplot(data, positions=years)

