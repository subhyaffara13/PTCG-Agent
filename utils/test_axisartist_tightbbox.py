
def test_axisartist_tightbbox():
    fig = plt.figure()
    tr = Affine2D().scale(np.pi / 180., 1.) + PolarAxes.PolarTransform()
    grid_helper = GridHelperCurveLinear(tr)
    ax = fig.add_subplot(axes_class=HostAxes, grid_helper=grid_helper)
    ax.axis["lon"] = ax.new_floating_axis(1, 9)

    ax.set_xlim(-5, 12)
    ax.set_ylim(-5, 10)

    ax.axis['lon'].major_ticklabels.set_visible(False)

    # Since the labels are invisible and the lines are clipped to the axes,
    # the axis's tight bbox should be contained in the axes box.
    renderer = fig._get_renderer()
    tight_points = ax.axis['lon'].get_tightbbox(renderer).get_points()
    for point in tight_points:
        assert ax.bbox.contains(*point)

