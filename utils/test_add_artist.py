
def test_add_artist(fig_test, fig_ref):
    fig_test.dpi = 100
    fig_ref.dpi = 100

    fig_test.subplots()
    l1 = plt.Line2D([.2, .7], [.7, .7], gid='l1')
    l2 = plt.Line2D([.2, .7], [.8, .8], gid='l2')
    r1 = plt.Circle((20, 20), 100, transform=None, gid='C1')
    r2 = plt.Circle((.7, .5), .05, gid='C2')
    r3 = plt.Circle((4.5, .8), .55, transform=fig_test.dpi_scale_trans,
                    facecolor='crimson', gid='C3')
    for a in [l1, l2, r1, r2, r3]:
        fig_test.add_artist(a)
    l2.remove()

    ax2 = fig_ref.subplots()
    l1 = plt.Line2D([.2, .7], [.7, .7], transform=fig_ref.transFigure,
                    gid='l1', zorder=21)
    r1 = plt.Circle((20, 20), 100, transform=None, clip_on=False, zorder=20,
                    gid='C1')
    r2 = plt.Circle((.7, .5), .05, transform=fig_ref.transFigure, gid='C2',
                    zorder=20)
    r3 = plt.Circle((4.5, .8), .55, transform=fig_ref.dpi_scale_trans,
                    facecolor='crimson', clip_on=False, zorder=20, gid='C3')
    for a in [l1, r1, r2, r3]:
        ax2.add_artist(a)

