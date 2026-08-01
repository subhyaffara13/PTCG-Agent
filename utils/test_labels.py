
def test_labels():
    assert lookup('utf-8').name == 'utf-8'
    assert lookup('Utf-8').name == 'utf-8'
    assert lookup('UTF-8').name == 'utf-8'
    assert lookup('utf8').name == 'utf-8'
    assert lookup('utf8').name == 'utf-8'
    assert lookup('utf8 ').name == 'utf-8'
    assert lookup(' \r\nutf8\t').name == 'utf-8'
    assert lookup('u8') is None  # Python label.
    assert lookup('utf-8 ') is None  # Non-ASCII white space.

    assert lookup('US-ASCII').name == 'windows-1252'
    assert lookup('iso-8859-1').name == 'windows-1252'
    assert lookup('latin1').name == 'windows-1252'
    assert lookup('LATIN1').name == 'windows-1252'
    assert lookup('latin-1') is None
    assert lookup('LATİN1') is None  # ASCII-only case insensitivity.


def test_labels(right, breaks, closed):
    arr = np.tile(np.arange(0, 1.01, 0.1), 4)

    result, bins = cut(arr, 4, retbins=True, right=right)
    ex_levels = IntervalIndex.from_breaks(breaks, closed=closed)
    tm.assert_index_equal(result.categories, ex_levels)


def test_labels():
    # Adapted from pylab_examples example code: contour_demo.py
    # see issues #2475, #2843, and #2818 for explanation
    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X**2 + Y**2) / 2) / (2 * np.pi)
    Z2 = (np.exp(-(((X - 1) / 1.5)**2 + ((Y - 1) / 0.5)**2) / 2) /
          (2 * np.pi * 0.5 * 1.5))

    # difference of Gaussians
    Z = 10.0 * (Z2 - Z1)

    fig, ax = plt.subplots(1, 1)
    CS = ax.contour(X, Y, Z)
    disp_units = [(216, 177), (359, 290), (521, 406)]
    data_units = [(-2, .5), (0, -1.5), (2.8, 1)]

    CS.clabel()

    for x, y in data_units:
        CS.add_label_near(x, y, inline=True, transform=None)

    for x, y in disp_units:
        CS.add_label_near(x, y, inline=True, transform=False)

