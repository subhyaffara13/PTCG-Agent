
def test_set_box_aspect_vertical_axis(vertical_axis, aspect_expected):
    ax = plt.subplot(1, 1, 1, projection="3d")
    ax.view_init(elev=0, azim=0, roll=0, vertical_axis=vertical_axis)
    ax.get_figure().canvas.draw()

    ax.set_box_aspect(None)

    np.testing.assert_allclose(aspect_expected, ax._box_aspect, rtol=1e-6)

