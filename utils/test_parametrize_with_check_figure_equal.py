
def test_parametrize_with_check_figure_equal(a, fig_ref, b, fig_test):
    fig_ref.add_subplot()
    fig_test.add_subplot()
    assert a == b

