
def test_axis_direction():
    # Check that axis direction is propagated on a floating axis
    fig = plt.figure()
    ax = Subplot(fig, 111)
    fig.add_subplot(ax)
    ax.axis['y'] = ax.new_floating_axis(nth_coord=1, value=0,
                                        axis_direction='left')
    assert ax.axis['y']._axis_direction == 'left'


def test_axis_direction():
    fig = plt.figure(figsize=(5, 5))

    # PolarAxes.PolarTransform takes radian. However, we want our coordinate
    # system in degree
    tr = Affine2D().scale(np.pi / 180., 1.) + PolarAxes.PolarTransform()

    # polar projection, which involves cycle, and also has limits in
    # its coordinates, needs a special method to find the extremes
    # (min, max of the coordinate within the view).

    # 20, 20 : number of sampling points along x, y direction
    extreme_finder = angle_helper.ExtremeFinderCycle(20, 20,
                                                     lon_cycle=360,
                                                     lat_cycle=None,
                                                     lon_minmax=None,
                                                     lat_minmax=(0, np.inf),
                                                     )

    grid_locator1 = angle_helper.LocatorDMS(12)
    tick_formatter1 = angle_helper.FormatterDMS()

    grid_helper = GridHelperCurveLinear(tr,
                                        extreme_finder=extreme_finder,
                                        grid_locator1=grid_locator1,
                                        tick_formatter1=tick_formatter1)

    ax1 = SubplotHost(fig, 1, 1, 1, grid_helper=grid_helper)

    for axis in ax1.axis.values():
        axis.set_visible(False)

    fig.add_subplot(ax1)

    ax1.axis["lat1"] = axis = grid_helper.new_floating_axis(
        0, 130,
        axes=ax1, axis_direction="left")
    axis.label.set_text("Test")
    axis.label.set_visible(True)
    axis.get_helper().set_extremes(0.001, 10)

    ax1.axis["lat2"] = axis = grid_helper.new_floating_axis(
        0, 50,
        axes=ax1, axis_direction="right")
    axis.label.set_text("Test")
    axis.label.set_visible(True)
    axis.get_helper().set_extremes(0.001, 10)

    ax1.axis["lon"] = axis = grid_helper.new_floating_axis(
        1, 10,
        axes=ax1, axis_direction="bottom")
    axis.label.set_text("Test 2")
    axis.get_helper().set_extremes(50, 130)
    axis.major_ticklabels.set_axis_direction("top")
    axis.label.set_axis_direction("top")

    grid_helper.grid_finder.grid_locator1.set_params(nbins=5)
    grid_helper.grid_finder.grid_locator2.set_params(nbins=5)

    ax1.set_aspect(1.)
    ax1.set_xlim(-8, 8)
    ax1.set_ylim(-4, 12)

    ax1.grid(True)

