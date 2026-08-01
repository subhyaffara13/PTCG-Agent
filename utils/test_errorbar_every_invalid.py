
def test_errorbar_every_invalid():
    x = np.linspace(0, 1, 15)
    y = x * (1-x)
    yerr = y/6

    ax = plt.figure().subplots()

    with pytest.raises(ValueError, match='not a tuple of two integers'):
        ax.errorbar(x, y, yerr, errorevery=(1, 2, 3))
    with pytest.raises(ValueError, match='not a tuple of two integers'):
        ax.errorbar(x, y, yerr, errorevery=(1.3, 3))
    with pytest.raises(ValueError, match='not a valid NumPy fancy index'):
        ax.errorbar(x, y, yerr, errorevery=[False, True])
    with pytest.raises(ValueError, match='not a recognized value'):
        ax.errorbar(x, y, yerr, errorevery='foobar')

