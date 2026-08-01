
def test_drawstyle_variants():
    fig, axs = plt.subplots(6)
    dss = ["default", "steps-mid", "steps-pre", "steps-post", "steps", None]
    # We want to check that drawstyles are properly handled even for very long
    # lines (for which the subslice optimization is on); however, we need
    # to zoom in so that the difference between the drawstyles is actually
    # visible.
    for ax, ds in zip(axs.flat, dss):
        ax.plot(range(2000), drawstyle=ds)
        ax.set(xlim=(0, 2), ylim=(0, 2))

