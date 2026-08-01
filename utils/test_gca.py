
def test_gca():
    fig = plt.figure()

    # test that gca() picks up Axes created via add_axes()
    ax0 = fig.add_axes((0, 0, 1, 1))
    assert fig.gca() is ax0

    # test that gca() picks up Axes created via add_subplot()
    ax1 = fig.add_subplot(111)
    assert fig.gca() is ax1

    # add_axes on an existing Axes should not change stored order, but will
    # make it current.
    fig.add_axes(ax0)
    assert fig.axes == [ax0, ax1]
    assert fig.gca() is ax0

    # sca() should not change stored order of Axes, which is order added.
    fig.sca(ax0)
    assert fig.axes == [ax0, ax1]

    # add_subplot on an existing Axes should not change stored order, but will
    # make it current.
    fig.add_subplot(ax1)
    assert fig.axes == [ax0, ax1]
    assert fig.gca() is ax1


def test_gca():
    # plt.gca() returns an existing axes, unless there were no axes.
    plt.figure()
    ax = plt.gca()
    ax1 = plt.gca()
    assert ax is not None
    assert ax1 is ax
    plt.close()

