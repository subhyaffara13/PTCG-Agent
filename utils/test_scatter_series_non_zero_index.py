
def test_scatter_series_non_zero_index(pd):
    # create non-zero index
    ids = range(10, 18)
    x = pd.Series(np.random.uniform(size=8), index=ids)
    y = pd.Series(np.random.uniform(size=8), index=ids)
    c = pd.Series([1, 1, 1, 1, 1, 0, 0, 0], index=ids)
    plt.scatter(x, y, c)

