
def test_contour_manual_moveto():
    x = np.linspace(-10, 10)
    y = np.linspace(-10, 10)

    X, Y = np.meshgrid(x, y)

    Z = X**2 * 1 / Y**2 - 1

    contours = plt.contour(X, Y, Z, levels=[0, 100])

    # This point lies on the `MOVETO` line for the 100 contour
    # but is actually closest to the 0 contour
    point = (1.3, 1)
    clabels = plt.clabel(contours, manual=[point])

    # Ensure that the 0 contour was chosen, not the 100 contour
    assert clabels[0].get_text() == "0"

