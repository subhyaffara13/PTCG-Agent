
def test_axes_kwargs():
    # plt.axes() always creates new axes, even if axes kwargs differ.
    plt.figure()
    ax = plt.axes()
    ax1 = plt.axes()
    assert ax is not None
    assert ax1 is not ax
    plt.close()

    plt.figure()
    ax = plt.axes(projection='polar')
    ax1 = plt.axes(projection='polar')
    assert ax is not None
    assert ax1 is not ax
    plt.close()

    plt.figure()
    ax = plt.axes(projection='polar')
    ax1 = plt.axes()
    assert ax is not None
    assert ax1.name == 'rectilinear'
    assert ax1 is not ax
    plt.close()

