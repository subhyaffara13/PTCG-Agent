
def test_legend_proper_window_extent():
    # test that legend returns the expected extent under various dpi...
    fig, ax = plt.subplots(dpi=100)
    ax.plot(range(10), label='Aardvark')
    leg = ax.legend()
    x01 = leg.get_window_extent(fig.canvas.get_renderer()).x0

    fig, ax = plt.subplots(dpi=200)
    ax.plot(range(10), label='Aardvark')
    leg = ax.legend()
    x02 = leg.get_window_extent(fig.canvas.get_renderer()).x0
    assert pytest.approx(x01*2, 0.1) == x02

