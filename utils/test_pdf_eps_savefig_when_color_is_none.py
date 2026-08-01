
def test_pdf_eps_savefig_when_color_is_none(fig_test, fig_ref):
    ax_test = fig_test.add_subplot()
    ax_test.set_axis_off()
    ax_test.plot(np.sin(np.linspace(-5, 5, 100)), "v", c="none")
    ax_ref = fig_ref.add_subplot()
    ax_ref.set_axis_off()

