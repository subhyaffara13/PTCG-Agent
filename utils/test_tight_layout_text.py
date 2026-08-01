
def test_tight_layout_text(fig_test, fig_ref):
    # text is currently ignored in tight layout. So the order of text() and
    # tight_layout() calls should not influence the result.
    ax1 = fig_test.add_subplot(projection='3d')
    ax1.text(.5, .5, .5, s='some string')
    fig_test.tight_layout()

    ax2 = fig_ref.add_subplot(projection='3d')
    fig_ref.tight_layout()
    ax2.text(.5, .5, .5, s='some string')

