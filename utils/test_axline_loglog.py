
def test_axline_loglog(fig_test, fig_ref):
    ax = fig_test.subplots()
    ax.set(xlim=(0.1, 10), ylim=(1e-3, 1))
    ax.loglog([.3, .6], [.3, .6], ".-")
    ax.axline((1, 1e-3), (10, 1e-2), c="k")

    ax = fig_ref.subplots()
    ax.set(xlim=(0.1, 10), ylim=(1e-3, 1))
    ax.loglog([.3, .6], [.3, .6], ".-")
    ax.loglog([1, 10], [1e-3, 1e-2], c="k")

