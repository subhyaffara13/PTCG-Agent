
def test_odd_dashes(fig_test, fig_ref):
    fig_test.add_subplot().plot([1, 2], dashes=[1, 2, 3])
    fig_ref.add_subplot().plot([1, 2], dashes=[1, 2, 3, 1, 2, 3])

