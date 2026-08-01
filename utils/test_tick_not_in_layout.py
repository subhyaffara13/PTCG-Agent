
def test_tick_not_in_layout(fig_test, fig_ref):
    # Check that the "very long" ticklabel is ignored from layouting after
    # set_in_layout(False); i.e. the layout is as if the ticklabel was empty.
    # Ticklabels are set to white so that the actual string doesn't matter.
    fig_test.set_layout_engine("constrained")
    ax = fig_test.add_subplot(xticks=[0, 1], xticklabels=["short", "very long"])
    ax.tick_params(labelcolor="w")
    fig_test.draw_without_rendering()  # Ensure ticks are correct.
    ax.xaxis.majorTicks[-1].label1.set_in_layout(False)
    fig_ref.set_layout_engine("constrained")
    ax = fig_ref.add_subplot(xticks=[0, 1], xticklabels=["short", ""])
    ax.tick_params(labelcolor="w")

