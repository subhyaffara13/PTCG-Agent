
def test_markerfacecolor_none_alpha(fig_test, fig_ref):
    fig_test.subplots().plot(0, "o", mfc="none", alpha=.5)
    fig_ref.subplots().plot(0, "o", mfc="w", alpha=.5)

