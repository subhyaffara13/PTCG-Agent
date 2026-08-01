
def test_operator_space(fig_test, fig_ref):
    fig_test.text(0.1, 0.1, r"$\log 6$")
    fig_test.text(0.1, 0.2, r"$\log(6)$")
    fig_test.text(0.1, 0.3, r"$\arcsin 6$")
    fig_test.text(0.1, 0.4, r"$\arcsin|6|$")
    fig_test.text(0.1, 0.5, r"$\operatorname{op} 6$")  # GitHub issue #553
    fig_test.text(0.1, 0.6, r"$\operatorname{op}[6]$")
    fig_test.text(0.1, 0.7, r"$\cos^2$")
    fig_test.text(0.1, 0.8, r"$\log_2$")
    fig_test.text(0.1, 0.9, r"$\sin^2 \max \cos$")  # GitHub issue #17852

    fig_ref.text(0.1, 0.1, r"$\mathrm{log\,}6$")
    fig_ref.text(0.1, 0.2, r"$\mathrm{log}(6)$")
    fig_ref.text(0.1, 0.3, r"$\mathrm{arcsin\,}6$")
    fig_ref.text(0.1, 0.4, r"$\mathrm{arcsin}|6|$")
    fig_ref.text(0.1, 0.5, r"$\mathrm{op\,}6$")
    fig_ref.text(0.1, 0.6, r"$\mathrm{op}[6]$")
    fig_ref.text(0.1, 0.7, r"$\mathrm{cos}^2$")
    fig_ref.text(0.1, 0.8, r"$\mathrm{log}_2$")
    fig_ref.text(0.1, 0.9, r"$\mathrm{sin}^2 \mathrm{\,max} \mathrm{\,cos}$")

