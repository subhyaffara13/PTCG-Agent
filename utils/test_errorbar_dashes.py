
def test_errorbar_dashes(fig_test, fig_ref):
    x = [1, 2, 3, 4]
    y = np.sin(x)

    ax_ref = fig_ref.gca()
    ax_test = fig_test.gca()

    line, *_ = ax_ref.errorbar(x, y, xerr=np.abs(y), yerr=np.abs(y))
    line.set_dashes([2, 2])

    ax_test.errorbar(x, y, xerr=np.abs(y), yerr=np.abs(y), dashes=[2, 2])

