
def test_axisbelow():
    # Test 'line' setting added in 6287.
    # Show only grids, not frame or ticks, to make this test
    # independent of future change to drawing order of those elements.
    axs = plt.figure().subplots(ncols=3, sharex=True, sharey=True)
    settings = (False, 'line', True)

    for ax, setting in zip(axs, settings):
        ax.plot((0, 10), (0, 10), lw=10, color='m')
        circ = mpatches.Circle((3, 3), color='r')
        ax.add_patch(circ)
        ax.grid(color='c', linestyle='-', linewidth=3)
        ax.tick_params(top=False, bottom=False,
                       left=False, right=False)
        ax.spines[:].set_visible(False)
        ax.set_axisbelow(setting)
        assert ax.get_axisbelow() == setting

