
def test_text_clip(fig_test, fig_ref):
    ax = fig_test.add_subplot()
    # Fully clipped-out text should not appear.
    ax.text(0, 0, "hello", transform=fig_test.transFigure, clip_on=True)
    fig_ref.add_subplot()

