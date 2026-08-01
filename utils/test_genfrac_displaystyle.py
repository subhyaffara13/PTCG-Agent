
def test_genfrac_displaystyle(fig_test, fig_ref):
    fig_test.text(0.1, 0.1, r"$\dfrac{2x}{3y}$")

    thickness = _mathtext.TruetypeFonts.get_underline_thickness(
        None, None, fontsize=mpl.rcParams["font.size"],
        dpi=mpl.rcParams["savefig.dpi"])
    fig_ref.text(0.1, 0.1, r"$\genfrac{}{}{%f}{0}{2x}{3y}$" % thickness)

