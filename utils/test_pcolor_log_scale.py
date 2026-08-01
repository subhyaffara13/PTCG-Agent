
def test_pcolor_log_scale(fig_test, fig_ref):
    """
    Check that setting a log scale sets good default axis limits
    when using pcolor.
    """
    x = np.linspace(0, 1, 11)
    # Ensuring second x value always falls slightly above 0.1 prevents flakiness with
    # numpy v1 #30882. This can be removed once we require numpy >= 2.
    x[1] += 0.00001
    y = np.linspace(1, 2, 5)
    X, Y = np.meshgrid(x, y)
    C = X[:-1, :-1] + Y[:-1, :-1]

    ax = fig_test.subplots()
    ax.pcolor(X, Y, C)
    ax.set_xscale('log')

    ax = fig_ref.subplots()
    ax.pcolor(X, Y, C)
    ax.set_xlim(1e-1, 1e0)
    ax.set_xscale('log')

