
def test_phantoms(fig_test, fig_ref):
    fig_test.text(0.5, 0.9, r"$\rlap{rlap}extra$", ha="left")
    fig_ref.text(0.5, 0.9, r"$rlap$", ha="left")
    fig_ref.text(0.5, 0.9, r"$extra$", ha="left")

    fig_test.text(0.5, 0.8, r"$extra\llap{llap}$", ha="right")
    fig_ref.text(0.5, 0.8, r"$llap$", ha="right")
    fig_ref.text(0.5, 0.8, r"$extra$", ha="right")

    fig_test.text(0.5, 0.7, r"$\phantom{phantom}$")

