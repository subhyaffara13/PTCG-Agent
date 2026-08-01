
def test_large_arc():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    x = 210
    y = -2115
    diameter = 4261
    for ax in [ax1, ax2]:
        a = Arc((x, y), diameter, diameter, lw=2, color='k')
        ax.add_patch(a)
        ax.set_axis_off()
        ax.set_aspect('equal')
    # force the high accuracy case
    ax1.set_xlim(7, 8)
    ax1.set_ylim(5, 6)

    # force the low accuracy case
    ax2.set_xlim(-25000, 18000)
    ax2.set_ylim(-20000, 6600)

