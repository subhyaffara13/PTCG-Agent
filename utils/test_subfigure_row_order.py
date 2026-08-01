
def test_subfigure_row_order():
    # Test that subfigures are drawn in row-major order.
    fig = plt.figure()
    sf_arr = fig.subfigures(4, 3)
    for a, b in zip(sf_arr.ravel(), fig.subfigs):
        assert a is b

