
def test_arc_spine_inner_no_axis():
    # Backcompat: smoke test that inner arc spine does not need a registered
    # axis in order to be drawn
    fig = plt.figure()
    ax = fig.add_subplot(projection="polar")
    inner_spine = ax.spines["inner"]
    inner_spine.register_axis(None)
    assert ax.spines["inner"].axis is None

    fig.draw_without_rendering()

