
def test_subsampled_ticklabels():
    # test issue 11937
    fig, ax = plt.subplots()
    ax.plot(np.arange(10))
    ax.xaxis.set_ticks(np.arange(10) + 0.1)
    ax.locator_params(nbins=5)
    ax.xaxis.set_ticklabels([c for c in "bcdefghijk"])
    plt.draw()
    labels = [t.get_text() for t in ax.xaxis.get_ticklabels()]
    assert labels == ['b', 'd', 'f', 'h', 'j']

