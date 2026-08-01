
def test_animated_with_canvas_change(fig_test, fig_ref):
    ax_ref = fig_ref.subplots()
    ax_ref.plot(range(5))

    ax_test = fig_test.subplots()
    ax_test.plot(range(5), animated=True)

