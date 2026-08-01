
def test_vline_limit():
    fig = plt.figure()
    ax = fig.gca()
    ax.axvline(0.5)
    ax.plot([-0.1, 0, 0.2, 0.1])
    assert_allclose(ax.get_ylim(), (-.1, .2))

