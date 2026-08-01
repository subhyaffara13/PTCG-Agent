
def test_contour_pre_transform_limits():
    ax = plt.axes()
    xs, ys = np.meshgrid(np.linspace(15, 20, 15), np.linspace(12.4, 12.5, 20))
    ax.contourf(xs, ys, np.log(xs * ys),
                transform=mtransforms.Affine2D().scale(0.1) + ax.transData)

    expected = np.array([[1.5, 1.24],
                         [2., 1.25]])
    assert_almost_equal(expected, ax.dataLim.get_points())

