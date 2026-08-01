
def _rc_test_bxp_helper(ax, rc_dict):
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    with matplotlib.rc_context(rc_dict):
        ax.boxplot([x, x])
    return ax

