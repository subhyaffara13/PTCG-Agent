
def test_legend_expand():
    """Test expand mode"""
    legend_modes = [None, "expand"]
    fig, axs = plt.subplots(len(legend_modes), 1)
    x = np.arange(100)
    for ax, mode in zip(axs, legend_modes):
        ax.plot(x, 50 - x, 'o', label='y=1')
        l1 = ax.legend(loc='upper left', mode=mode)
        ax.add_artist(l1)
        ax.plot(x, x - 50, 'o', label='y=-1')
        l2 = ax.legend(loc='right', mode=mode)
        ax.add_artist(l2)
        ax.legend(loc='lower left', mode=mode, ncols=2)

