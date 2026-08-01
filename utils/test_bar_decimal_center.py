
def test_bar_decimal_center(fig_test, fig_ref):
    ax = fig_test.subplots()
    x0 = [1.5, 8.4, 5.3, 4.2]
    y0 = [1.1, 2.2, 3.3, 4.4]
    x = [Decimal(x) for x in x0]
    y = [Decimal(y) for y in y0]
    # Test image - vertical, align-center bar chart with Decimal() input
    ax.bar(x, y, align='center')
    # Reference image
    ax = fig_ref.subplots()
    ax.bar(x0, y0, align='center')

