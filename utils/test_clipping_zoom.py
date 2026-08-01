
def test_clipping_zoom(fig_test, fig_ref):
    # This test places the Axes and sets its limits such that the clip path is
    # outside the figure entirely. This should not break the clip path.
    ax_test = fig_test.add_axes((0, 0, 1, 1))
    l, = ax_test.plot([-3, 3], [-3, 3])
    # Explicit Path instead of a Rectangle uses clip path processing, instead
    # of a clip box optimization.
    p = mpath.Path([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    p = mpatches.PathPatch(p, transform=ax_test.transData)
    l.set_clip_path(p)

    ax_ref = fig_ref.add_axes((0, 0, 1, 1))
    ax_ref.plot([-3, 3], [-3, 3])

    ax_ref.set(xlim=(0.5, 0.75), ylim=(0.5, 0.75))
    ax_test.set(xlim=(0.5, 0.75), ylim=(0.5, 0.75))

