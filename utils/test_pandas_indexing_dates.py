
def test_pandas_indexing_dates(pd):
    dates = np.arange('2005-02', '2005-03', dtype='datetime64[D]')
    values = np.sin(range(len(dates)))
    df = pd.DataFrame({'dates': dates, 'values': values})

    ax = plt.gca()

    without_zero_index = df[np.array(df.index) % 2 == 1].copy()
    ax.plot('dates', 'values', data=without_zero_index)

