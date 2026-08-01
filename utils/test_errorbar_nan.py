
def test_errorbar_nan(fig_test, fig_ref):
    ax = fig_test.add_subplot()
    xs = range(5)
    ys = np.array([1, 2, np.nan, np.nan, 3])
    es = np.array([4, 5, np.nan, np.nan, 6])
    ax.errorbar(xs, ys, yerr=es)
    ax = fig_ref.add_subplot()
    ax.errorbar([0, 1], [1, 2], yerr=[4, 5])
    ax.errorbar([4], [3], yerr=[6], fmt="C0")

