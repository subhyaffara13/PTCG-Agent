
def test_circular_contour_warning():
    # Check that almost circular contours don't throw a warning
    x, y = np.meshgrid(np.linspace(-2, 2, 4), np.linspace(-2, 2, 4))
    r = np.hypot(x, y)
    plt.figure()
    cs = plt.contour(x, y, r)
    plt.clabel(cs)

