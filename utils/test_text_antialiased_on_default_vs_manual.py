
def test_text_antialiased_on_default_vs_manual(fig_test, fig_ref):
    fig_test.text(0.5, 0.5, '6 inches x 2 inches', antialiased=True)

    mpl.rcParams['text.antialiased'] = True
    fig_ref.text(0.5, 0.5, '6 inches x 2 inches')

