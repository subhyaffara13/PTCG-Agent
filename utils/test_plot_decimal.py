
def test_plot_decimal(fig_test, fig_ref):
    x0 = np.arange(-10, 10, 0.3)
    y0 = [5.2 * x ** 3 - 2.1 * x ** 2 + 7.34 * x + 4.5 for x in x0]
    x = [Decimal(i) for i in x0]
    y = [Decimal(i) for i in y0]
    # Test image - line plot with Decimal input
    fig_test.subplots().plot(x, y)
    # Reference image
    fig_ref.subplots().plot(x0, y0)

