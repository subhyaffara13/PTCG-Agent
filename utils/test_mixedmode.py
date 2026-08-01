
def test_mixedmode():
    mpl.rcParams.update({'font.family': 'serif', 'pgf.rcfonts': False})
    Y, X = np.ogrid[-1:1:40j, -1:1:40j]
    plt.pcolor(X**2 + Y**2).set_rasterized(True)

