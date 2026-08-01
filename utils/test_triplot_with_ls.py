
def test_triplot_with_ls(fig_test, fig_ref):
    x = [0, 2, 1]
    y = [0, 0, 1]
    data = [[0, 1, 2]]
    fig_test.subplots().triplot(x, y, data, ls='--')
    fig_ref.subplots().triplot(x, y, data, linestyle='--')

