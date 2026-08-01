
def test_marker_edges():
    x = np.linspace(0, 1, 10)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'y.', ms=30.0, mew=0, mec='r')
    ax.plot(x+0.1, np.sin(x), 'y.', ms=30.0, mew=1, mec='r')
    ax.plot(x+0.2, np.sin(x), 'y.', ms=30.0, mew=2, mec='b')

