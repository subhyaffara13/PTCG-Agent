
def test_shared_scale():
    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)

    axs[0, 0].set_xscale("log")
    axs[0, 0].set_yscale("log")

    for ax in axs.flat:
        assert ax.get_yscale() == 'log'
        assert ax.get_xscale() == 'log'

    axs[1, 1].set_xscale("linear")
    axs[1, 1].set_yscale("linear")

    for ax in axs.flat:
        assert ax.get_yscale() == 'linear'
        assert ax.get_xscale() == 'linear'

