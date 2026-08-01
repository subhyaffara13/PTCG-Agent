
def test_rgb_axes():
    fig = plt.figure()
    ax = RGBAxes(fig, (0.1, 0.1, 0.8, 0.8), pad=0.1)
    rng = np.random.default_rng(19680801)
    r = rng.random((5, 5))
    g = rng.random((5, 5))
    b = rng.random((5, 5))
    ax.imshow_rgb(r, g, b, interpolation='none')

