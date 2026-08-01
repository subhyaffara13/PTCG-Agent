
def test_spine_nonlinear_data_positions(fig_test, fig_ref):
    plt.style.use("default")

    ax = fig_test.add_subplot()
    ax.set(xscale="log", xlim=(.1, 1))
    # Use position="data" to visually swap the left and right spines, using
    # linewidth to distinguish them.  The calls to tick_params removes labels
    # (for image comparison purposes) and harmonizes tick positions with the
    # reference).
    ax.spines.left.set_position(("data", 1))
    ax.spines.left.set_linewidth(2)
    ax.spines.right.set_position(("data", .1))
    ax.tick_params(axis="y", labelleft=False, direction="in")

    ax = fig_ref.add_subplot()
    ax.set(xscale="log", xlim=(.1, 1))
    ax.spines.right.set_linewidth(2)
    ax.tick_params(axis="y", labelleft=False, left=False, right=True)

