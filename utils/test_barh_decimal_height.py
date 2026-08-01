
def test_barh_decimal_height(fig_test, fig_ref):
    x = [1.5, 8.4, 5.3, 4.2]
    y = [1.1, 2.2, 3.3, 4.4]
    h0 = [0.7, 1.45, 1, 2]
    h = [Decimal(i) for i in h0]
    # Test image - horizontal bar chart with Decimal() height
    ax = fig_test.subplots()
    ax.barh(x, y, height=h, align='center')
    # Reference image
    ax = fig_ref.subplots()
    ax.barh(x, y, height=h0, align='center')

