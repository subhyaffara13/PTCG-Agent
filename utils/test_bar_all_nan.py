
def test_bar_all_nan(fig_test, fig_ref):
    mpl.style.use("mpl20")
    ax_test = fig_test.subplots()
    ax_ref = fig_ref.subplots()

    ax_test.bar([np.nan], [np.nan])
    ax_test.bar([1], [1])

    ax_ref.bar([1], [1]).remove()
    ax_ref.bar([1], [1])

