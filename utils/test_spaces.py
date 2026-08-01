
def test_spaces(fig_test, fig_ref):
    fig_test.text(.5, .5, r"$1\,2\>3\ 4$")
    fig_ref.text(.5, .5, r"$1\/2\:3~4$")

