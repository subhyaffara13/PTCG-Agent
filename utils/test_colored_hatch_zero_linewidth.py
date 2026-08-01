
def test_colored_hatch_zero_linewidth():
    ax = plt.gca()
    ax.add_patch(Ellipse((0, 0), 1, 1, hatch='/', facecolor='none',
                         edgecolor='r', linewidth=0))
    ax.add_patch(Ellipse((0.5, 0.5), 0.5, 0.5, hatch='+', facecolor='none',
                         edgecolor='g', linewidth=0.2))
    ax.add_patch(Ellipse((1, 1), 0.3, 0.8, hatch='\\', facecolor='none',
                         edgecolor='b', linewidth=0))
    ax.set_axis_off()

