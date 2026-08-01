
def test_boxplot_masked(fig_test, fig_ref):
    # Check that masked values are ignored when plotting a boxplot
    x_orig = np.linspace(-1, 1, 200)

    ax = fig_test.subplots()
    x = x_orig[x_orig >= 0]
    ax.boxplot(x)

    x = np.ma.masked_less(x_orig, 0)
    ax = fig_ref.subplots()
    ax.boxplot(x)

