
def test_unicode_minus(fig_test, fig_ref):
    mpl.rcParams['text.usetex'] = True
    fig_test.text(.5, .5, "$-$")
    fig_ref.text(.5, .5, "\N{MINUS SIGN}")

