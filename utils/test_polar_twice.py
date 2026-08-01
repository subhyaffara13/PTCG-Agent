
def test_polar_twice():
    fig = plt.figure()
    plt.polar([1, 2], [.1, .2])
    plt.polar([3, 4], [.3, .4])
    assert len(fig.axes) == 1, 'More than one polar Axes created.'

