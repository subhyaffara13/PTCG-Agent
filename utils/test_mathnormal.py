
def test_mathnormal(fig_test, fig_ref):
    # ensure that \mathnormal is parsed and sets digits upright
    fig_test.text(0.1, 0.2, r"$\mathnormal{0123456789}$")
    fig_ref.text(0.1, 0.2, r"$\mathrm{0123456789}$")

