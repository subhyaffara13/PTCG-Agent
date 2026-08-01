
def test_minorticks_on_rcParams_both(fig_test, fig_ref):
    with matplotlib.rc_context({"xtick.minor.visible": True,
                                "ytick.minor.visible": True}):
        ax_test = fig_test.subplots()
        ax_test.plot([0, 1], [0, 1])
    ax_ref = fig_ref.subplots()
    ax_ref.plot([0, 1], [0, 1])
    ax_ref.minorticks_on()

