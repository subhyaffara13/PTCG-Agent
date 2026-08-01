
def test_bbox_inches():
    mpl.rcParams.update({'font.family': 'serif', 'pgf.rcfonts': False})
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(range(5))
    ax2.plot(range(5))
    plt.tight_layout()
    bbox = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    compare_figure('pgf_bbox_inches.pdf', savefig_kwargs={'bbox_inches': bbox},
                   tol=0)

