
def test_radial_locator_wrapping():
    # Check that the locator is always wrapped inside a RadialLocator
    # and that RaidialAxis.isDefault_majloc is set correctly.
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    assert ax.yaxis.isDefault_majloc
    assert isinstance(ax.yaxis.get_major_locator(), RadialLocator)

    # set an explicit locator
    locator = mticker.MaxNLocator(3)
    ax.yaxis.set_major_locator(locator)
    assert not ax.yaxis.isDefault_majloc
    assert isinstance(ax.yaxis.get_major_locator(), RadialLocator)
    assert ax.yaxis.get_major_locator().base is locator

    ax.clear()  # reset to the default locator
    assert ax.yaxis.isDefault_majloc
    assert isinstance(ax.yaxis.get_major_locator(), RadialLocator)

    ax.set_rticks([0, 1, 2, 3])  # implicitly sets a FixedLocator
    assert not ax.yaxis.isDefault_majloc  # because of the fixed ticks
    assert isinstance(ax.yaxis.get_major_locator(), RadialLocator)
    assert isinstance(ax.yaxis.get_major_locator().base, mticker.FixedLocator)

    ax.clear()

    ax.set_rgrids([0, 1, 2, 3])  # implicitly sets a FixedLocator
    assert not ax.yaxis.isDefault_majloc  # because of the fixed ticks
    assert isinstance(ax.yaxis.get_major_locator(), RadialLocator)
    assert isinstance(ax.yaxis.get_major_locator().base, mticker.FixedLocator)

    ax.clear()

    ax.set_yscale("log")  # implicitly sets a LogLocator
    # Note that the LogLocator is still considered the default locator
    # for the log scale
    assert ax.yaxis.isDefault_majloc
    assert isinstance(ax.yaxis.get_major_locator(), RadialLocator)
    assert isinstance(ax.yaxis.get_major_locator().base, mticker.LogLocator)

