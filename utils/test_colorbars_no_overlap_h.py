
def test_colorbars_no_overlapH():
    fig = plt.figure(figsize=(4, 2), layout="constrained")
    fig.suptitle("foo")
    axs = fig.subplots(1, 2, sharex=True, sharey=True)
    for ax in axs:
        ax.yaxis.set_major_formatter(ticker.NullFormatter())
        ax.tick_params(axis='both', direction='in')
        im = ax.imshow([[1, 2], [3, 4]])
        fig.colorbar(im, ax=ax, orientation="horizontal")

