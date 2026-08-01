
def test_bar_hatches(fig_test, fig_ref):
    ax_test = fig_test.subplots()
    ax_ref = fig_ref.subplots()

    x = [1, 2]
    y = [2, 3]
    hatches = ['x', 'o']
    for i in range(2):
        ax_ref.bar(x[i], y[i], color='C0', hatch=hatches[i])

    ax_test.bar(x, y, hatch=hatches)

