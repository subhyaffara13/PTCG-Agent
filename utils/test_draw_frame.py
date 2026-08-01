
def test_draw_frame(return_value):
    # test _draw_frame method

    fig, ax = plt.subplots()
    line, = ax.plot([])

    def animate(i):
        # general update func
        line.set_data([0, 1], [0, i])
        if return_value == 'artist':
            # *not* a sequence
            return line
        else:
            return return_value

    with pytest.raises(RuntimeError):
        animation.FuncAnimation(
            fig, animate, blit=True, cache_frame_data=False
        )

