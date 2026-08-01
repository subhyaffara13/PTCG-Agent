
def test_bar_decimal_width(fig_test, fig_ref):
    x = [1.5, 8.4, 5.3, 4.2]
    y = [1.1, 2.2, 3.3, 4.4]
    w0 = [0.7, 1.45, 1, 2]
    w = [Decimal(i) for i in w0]
    # Test image - vertical bar chart with Decimal() width
    ax = fig_test.subplots()
    ax.bar(x, y, width=w, align='center')
    # Reference image
    ax = fig_ref.subplots()
    ax.bar(x, y, width=w0, align='center')

