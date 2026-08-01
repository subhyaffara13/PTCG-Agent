
def test_colorbars_no_overlapV():
    fig = plt.figure(figsize=(2, 4), layout="constrained")
    axs = fig.subplots(2, 1, sharex=True, sharey=True)
    for ax in axs:
        ax.yaxis.set_major_formatter(ticker.NullFormatter())
        ax.tick_params(axis='both', direction='in')
        im = ax.imshow([[1, 2], [3, 4]])
        fig.colorbar(im, ax=ax, orientation="vertical")
    fig.suptitle("foo")

