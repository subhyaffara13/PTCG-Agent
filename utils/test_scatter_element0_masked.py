
def test_scatter_element0_masked():
    times = np.arange('2005-02', '2005-03', dtype='datetime64[D]')
    y = np.arange(len(times), dtype=float)
    y[0] = np.nan
    fig, ax = plt.subplots()
    ax.scatter(times, y)
    fig.canvas.draw()

