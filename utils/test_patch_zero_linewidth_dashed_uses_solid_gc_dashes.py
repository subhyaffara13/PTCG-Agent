
def test_patch_zero_linewidth_dashed_uses_solid_gc_dashes():
    fig, ax = plt.subplots()
    ax.add_patch(Rectangle(
        (0, 0), 1, 1, fill=False, linewidth=0, linestyle='--'))
    fig.draw_without_rendering()

