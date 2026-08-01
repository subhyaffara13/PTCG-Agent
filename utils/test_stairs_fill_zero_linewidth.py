
def test_stairs_fill_zero_linewidth(fig_test, fig_ref):
    fig_test.subplots().stairs(
        [1, 2, 3, 4], [1, 2, 3, 4, 5], fill=True, ls='--')
    fig_ref.subplots().stairs(
        [1, 2, 3, 4], [1, 2, 3, 4, 5], fill=True, ls='-')

