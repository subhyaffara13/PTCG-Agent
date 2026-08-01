
def test_twin_logscale(fig_test, fig_ref, twin):
    twin_func = f'twin{twin}'  # test twinx or twiny
    set_scale = f'set_{twin}scale'
    x = np.arange(1, 100)

    # Change scale after twinning.
    ax_test = fig_test.add_subplot(2, 1, 1)
    ax_twin = getattr(ax_test, twin_func)()
    getattr(ax_test, set_scale)('log')
    ax_twin.plot(x, x)

    # Twin after changing scale.
    ax_test = fig_test.add_subplot(2, 1, 2)
    getattr(ax_test, set_scale)('log')
    ax_twin = getattr(ax_test, twin_func)()
    ax_twin.plot(x, x)

    for i in [1, 2]:
        ax_ref = fig_ref.add_subplot(2, 1, i)
        getattr(ax_ref, set_scale)('log')
        ax_ref.plot(x, x)

        # This is a hack because twinned Axes double-draw the frame.
        # Remove this when that is fixed.
        Path = matplotlib.path.Path
        fig_ref.add_artist(
            matplotlib.patches.PathPatch(
                Path([[0, 0], [0, 1],
                      [0, 1], [1, 1],
                      [1, 1], [1, 0],
                      [1, 0], [0, 0]],
                     [Path.MOVETO, Path.LINETO] * 4),
                transform=ax_ref.transAxes,
                facecolor='none',
                edgecolor=mpl.rcParams['axes.edgecolor'],
                linewidth=mpl.rcParams['axes.linewidth'],
                capstyle='projecting'))

    remove_ticks_and_titles(fig_test)
    remove_ticks_and_titles(fig_ref)

