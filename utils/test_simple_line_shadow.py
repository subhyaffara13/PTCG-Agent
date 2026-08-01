
def test_simple_line_shadow(fig_test, fig_ref):
    ax_ref = fig_ref.add_subplot()
    ax_test = fig_test.add_subplot()

    x = np.linspace(-5, 5, 500)
    y = np.exp(-x**2)

    line, = ax_test.plot(
        x, y, linewidth=5,
        path_effects=[
            path_effects.SimpleLineShadow(offset=(0, 0), shadow_color='blue')])

    ax_ref.plot(x, y, linewidth=5, color='blue', alpha=0.3)

