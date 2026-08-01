
def test_stackplot_hatching(fig_ref, fig_test):
    x = np.linspace(0, 10, 10)
    y1 = 1.0 * x
    y2 = 2.0 * x + 1
    y3 = 3.0 * x + 2
    # stackplot with different hatching styles (issue #27146)
    ax_test = fig_test.subplots()
    ax_test.stackplot(x, y1, y2, y3, hatch=["x", "//", "\\\\"], colors=["white"])
    ax_test.set_xlim(0, 10)
    ax_test.set_ylim(0, 70)
    # compare with result from hatching each layer individually
    stack_baseline = np.zeros(len(x))
    ax_ref = fig_ref.subplots()
    ax_ref.fill_between(x, stack_baseline, y1, hatch="x", facecolor="white")
    ax_ref.fill_between(x, y1, y1+y2, hatch="//", facecolor="white")
    ax_ref.fill_between(x, y1+y2, y1+y2+y3, hatch="\\\\", facecolor="white")
    ax_ref.set_xlim(0, 10)
    ax_ref.set_ylim(0, 70)

