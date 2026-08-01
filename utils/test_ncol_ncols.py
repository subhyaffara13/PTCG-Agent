
def test_ncol_ncols(fig_test, fig_ref):
    # Test that both ncol and ncols work
    strings = ["a", "b", "c", "d", "e", "f"]
    ncols = 3
    fig_test.legend(strings, ncol=ncols)
    fig_ref.legend(strings, ncols=ncols)

