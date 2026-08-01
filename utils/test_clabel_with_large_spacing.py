
def test_clabel_with_large_spacing():
    # When the inline spacing is large relative to the contour, it may cause the
    # entire contour to be removed. In current implementation, one line segment is
    # retained between the identified points.
    # This behavior may be worth reconsidering, but check to be sure we do not produce
    # an invalid path, which results in an error at clabel call time.
    # see gh-27045 for more information
    x = y = np.arange(-3.0, 3.01, 0.05)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-X**2 - Y**2)

    fig, ax = plt.subplots()
    contourset = ax.contour(X, Y, Z, levels=[0.01, 0.2, .5, .8])
    ax.clabel(contourset, inline_spacing=100)

