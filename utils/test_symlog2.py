
def test_symlog2():
    # Numbers from -50 to 50, with 0.1 as step
    x = np.arange(-50, 50, 0.001)

    fig, axs = plt.subplots(5, 1)
    for ax, linthresh in zip(axs, [20., 2., 1., 0.1, 0.01]):
        ax.plot(x, x)
        ax.set_xscale('symlog', linthresh=linthresh)
        ax.grid(True)
    axs[-1].set_ylim(-0.1, 0.1)

