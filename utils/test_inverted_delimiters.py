
def test_inverted_delimiters(fig_test, fig_ref):
    fig_test.text(.5, .5, r"$\left)\right($", math_fontfamily="dejavusans")
    fig_ref.text(.5, .5, r"$)($", math_fontfamily="dejavusans")

