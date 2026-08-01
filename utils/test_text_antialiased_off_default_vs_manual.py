
def test_text_antialiased_off_default_vs_manual(fig_test, fig_ref):
    fig_test.text(0.5, 0.5, '6 inches x 2 inches',
                             antialiased=False)

    mpl.rcParams['text.antialiased'] = False
    fig_ref.text(0.5, 0.5, '6 inches x 2 inches')

