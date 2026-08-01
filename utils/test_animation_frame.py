
def test_animation_frame(tmp_path, fig_test, fig_ref):
    # Test the expected image after iterating through a few frames
    # we save the animation to get the iteration because we are not
    # in an interactive framework.
    ax = fig_test.add_subplot()
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1, 1)
    x = np.linspace(0, 2 * np.pi, 100)
    line, = ax.plot([], [])

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        line.set_data(x, np.sin(x + i / 100))
        return line,

    anim = animation.FuncAnimation(
        fig_test, animate, init_func=init, frames=5,
        blit=True, repeat=False)
    anim.save(tmp_path / "test.gif")

    # Reference figure without animation
    ax = fig_ref.add_subplot()
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1, 1)

    # 5th frame's data
    ax.plot(x, np.sin(x + 4 / 100))

