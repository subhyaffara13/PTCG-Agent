
def test_chunksize():
    x = range(200)

    # Test without chunksize
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))
    fig.canvas.draw()

    # Test with chunksize
    fig, ax = plt.subplots()
    rcParams['agg.path.chunksize'] = 105
    ax.plot(x, np.sin(x))
    fig.canvas.draw()

