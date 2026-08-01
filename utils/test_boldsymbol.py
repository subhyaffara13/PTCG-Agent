
def test_boldsymbol(fig_test, fig_ref):
    fig_test.text(0.1, 0.2, r"$\boldsymbol{\mathrm{abc0123\alpha}}$")
    fig_ref.text(0.1, 0.2, r"$\mathrm{abc0123\alpha}$")

