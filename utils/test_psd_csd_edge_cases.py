
def test_psd_csd_edge_cases():
    # Inverted yaxis or fully zero inputs used to throw exceptions.
    axs = plt.figure().subplots(2)
    for ax in axs:
        ax.yaxis.set(inverted=True)
    with np.errstate(divide="ignore"):
        axs[0].psd(np.zeros(5))
        axs[1].csd(np.zeros(5), np.zeros(5))

