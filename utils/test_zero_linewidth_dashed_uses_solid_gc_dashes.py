
def test_zero_linewidth_dashed_uses_solid_gc_dashes():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], ls='--', lw=0)
    fig.draw_without_rendering()

