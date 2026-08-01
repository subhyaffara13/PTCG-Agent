
def test_square_plot():
    x = np.arange(4)
    y = np.array([1., 3., 5., 7.])
    fig, ax = plt.subplots()
    ax.plot(x, y, 'mo')
    ax.axis('square')
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    assert np.diff(xlim) == np.diff(ylim)
    assert ax.get_aspect() == 1
    assert_array_almost_equal(
        ax.get_position(original=True).extents, (0.125, 0.1, 0.9, 0.9))
    assert_array_almost_equal(
        ax.get_position(original=False).extents, (0.2125, 0.1, 0.8125, 0.9))

