
def test_textarea_set_text(fig_test, fig_ref):
    ax_ref = fig_ref.add_subplot()
    text0 = AnchoredText("Foo", "upper left")
    ax_ref.add_artist(text0)

    ax_test = fig_test.add_subplot()
    text1 = AnchoredText("Bar", "upper left")
    ax_test.add_artist(text1)
    text1.txt.set_text("Foo")

