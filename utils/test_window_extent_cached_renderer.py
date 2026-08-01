
def test_window_extent_cached_renderer():
    fig, ax = plt.subplots(dpi=100)
    ax.plot(range(10), label='Aardvark')
    leg = ax.legend()
    leg2 = fig.legend()
    fig.canvas.draw()
    # check that get_window_extent will use the cached renderer
    leg.get_window_extent()
    leg2.get_window_extent()

