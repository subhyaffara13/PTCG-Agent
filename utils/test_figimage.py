
def test_figimage(suppressComposite):
    fig = plt.figure(figsize=(2, 2), dpi=100)
    fig.suppressComposite = suppressComposite
    x, y = np.ix_(np.arange(100) / 100.0, np.arange(100) / 100)
    z = np.sin(x**2 + y**2 - x*y)
    c = np.sin(20*x**2 + 50*y**2)
    img = z + c/5

    fig.figimage(img, xo=0, yo=0, origin='lower')
    fig.figimage(img[::-1, :], xo=0, yo=100, origin='lower')
    fig.figimage(img[:, ::-1], xo=100, yo=0, origin='lower')
    fig.figimage(img[::-1, ::-1], xo=100, yo=100, origin='lower')

