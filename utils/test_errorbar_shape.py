
def test_errorbar_shape():
    fig = plt.figure()
    ax = fig.gca()

    x = np.arange(0.1, 4, 0.5)
    y = np.exp(-x)
    yerr1 = 0.1 + 0.2*np.sqrt(x)
    yerr = np.vstack((yerr1, 2*yerr1)).T
    xerr = 0.1 + yerr

    with pytest.raises(ValueError):
        ax.errorbar(x, y, yerr=yerr, fmt='o')
    with pytest.raises(ValueError):
        ax.errorbar(x, y, xerr=xerr, fmt='o')
    with pytest.raises(ValueError):
        ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='o')

