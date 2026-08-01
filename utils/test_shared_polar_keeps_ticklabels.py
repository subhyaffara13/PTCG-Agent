
def test_shared_polar_keeps_ticklabels():
    fig, axs = plt.subplots(
        2, 2, subplot_kw={"projection": "polar"}, sharex=True, sharey=True)
    fig.canvas.draw()
    assert axs[0, 1].xaxis.majorTicks[0].get_visible()
    assert axs[0, 1].yaxis.majorTicks[0].get_visible()
    fig, axs = plt.subplot_mosaic(
        "ab\ncd", subplot_kw={"projection": "polar"}, sharex=True, sharey=True)
    fig.canvas.draw()
    assert axs["b"].xaxis.majorTicks[0].get_visible()
    assert axs["b"].yaxis.majorTicks[0].get_visible()

