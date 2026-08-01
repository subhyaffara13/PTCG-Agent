
def test_default_thetalocator():
    # Ideally we would check AAAABBC, but the smallest axes currently puts a
    # single tick at 150° because MaxNLocator doesn't have a way to accept 15°
    # while rejecting 150°.
    fig, axs = plt.subplot_mosaic(
        "AAAABB.", subplot_kw={"projection": "polar"})
    for ax in axs.values():
        ax.set_thetalim(0, np.pi)
    for ax in axs.values():
        ticklocs = np.degrees(ax.xaxis.get_majorticklocs()).tolist()
        assert pytest.approx(90) in ticklocs
        assert pytest.approx(100) not in ticklocs

