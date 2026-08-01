
def test_add_axes_kwargs():
    # fig.add_axes() always creates new axes, even if axes kwargs differ.
    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1))
    ax1 = fig.add_axes((0, 0, 1, 1))
    assert ax is not None
    assert ax1 is not ax
    plt.close()

    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1), projection='polar')
    ax1 = fig.add_axes((0, 0, 1, 1), projection='polar')
    assert ax is not None
    assert ax1 is not ax
    plt.close()

    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1), projection='polar')
    ax1 = fig.add_axes((0, 0, 1, 1))
    assert ax is not None
    assert ax1.name == 'rectilinear'
    assert ax1 is not ax
    plt.close()

