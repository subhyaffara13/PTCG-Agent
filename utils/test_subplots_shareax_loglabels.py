
def test_subplots_shareax_loglabels():
    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, squeeze=False)
    for ax in axs.flat:
        ax.plot([10, 20, 30], [10, 20, 30])

    ax.set_yscale("log")
    ax.set_xscale("log")

    for ax in axs[0, :]:
        assert 0 == len(ax.xaxis.get_ticklabels(which='both'))

    for ax in axs[1, :]:
        assert 0 < len(ax.xaxis.get_ticklabels(which='both'))

    for ax in axs[:, 1]:
        assert 0 == len(ax.yaxis.get_ticklabels(which='both'))

    for ax in axs[:, 0]:
        assert 0 < len(ax.yaxis.get_ticklabels(which='both'))

