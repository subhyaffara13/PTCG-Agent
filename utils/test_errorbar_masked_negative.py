
def test_errorbar_masked_negative(fig_test, fig_ref):
    ax = fig_test.add_subplot()
    xs = range(5)
    mask = np.array([False, False, True, True, False])
    ys = np.ma.array([1, 2, 2, 2, 3], mask=mask)
    es = np.ma.array([4, 5, -1, -10, 6], mask=mask)
    ax.errorbar(xs, ys, yerr=es)
    ax = fig_ref.add_subplot()
    ax.errorbar([0, 1], [1, 2], yerr=[4, 5])
    ax.errorbar([4], [3], yerr=[6], fmt="C0")

