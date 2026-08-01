
def test_EllipseCollection_setter_getter():
    # Test widths, heights and angle setter
    rng = np.random.default_rng(0)

    widths = (2, )
    heights = (3, )
    angles = (45, )
    offsets = rng.random((10, 2)) * 10

    fig, ax = plt.subplots()

    ec = mcollections.EllipseCollection(
        widths=widths,
        heights=heights,
        angles=angles,
        offsets=offsets,
        units='x',
        offset_transform=ax.transData,
        )

    assert_array_almost_equal(ec._widths, np.array(widths).ravel() * 0.5)
    assert_array_almost_equal(ec._heights, np.array(heights).ravel() * 0.5)
    assert_array_almost_equal(ec._angles, np.deg2rad(angles).ravel())

    assert_array_almost_equal(ec.get_widths(), widths)
    assert_array_almost_equal(ec.get_heights(), heights)
    assert_array_almost_equal(ec.get_angles(), angles)

    ax.add_collection(ec)
    ax.set_xlim(-2, 12)
    ax.set_ylim(-2, 12)

    new_widths = rng.random((10, 2)) * 2
    new_heights = rng.random((10, 2)) * 3
    new_angles = rng.random((10, 2)) * 180

    ec.set(widths=new_widths, heights=new_heights, angles=new_angles)

    assert_array_almost_equal(ec.get_widths(), new_widths.ravel())
    assert_array_almost_equal(ec.get_heights(), new_heights.ravel())
    assert_array_almost_equal(ec.get_angles(), new_angles.ravel())

