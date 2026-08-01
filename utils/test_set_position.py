
def test_set_position():
    fig, ax = plt.subplots()
    ax.set_aspect(3.)
    ax.set_position([0.1, 0.1, 0.4, 0.4], which='both')
    assert np.allclose(ax.get_position().width, 0.1)
    ax.set_aspect(2.)
    ax.set_position([0.1, 0.1, 0.4, 0.4], which='original')
    assert np.allclose(ax.get_position().width, 0.15)
    ax.set_aspect(3.)
    ax.set_position([0.1, 0.1, 0.4, 0.4], which='active')
    assert np.allclose(ax.get_position().width, 0.1)


def test_set_position():
    fig, ax = plt.subplots()

    # test set_position
    ann = ax.annotate(
        'test', (0, 0), xytext=(0, 0), textcoords='figure pixels')
    fig.canvas.draw()

    init_pos = ann.get_window_extent(fig.canvas.renderer)
    shift_val = 15
    ann.set_position((shift_val, shift_val))
    fig.canvas.draw()
    post_pos = ann.get_window_extent(fig.canvas.renderer)

    for a, b in zip(init_pos.min, post_pos.min):
        assert a + shift_val == b

    # test xyann
    ann = ax.annotate(
        'test', (0, 0), xytext=(0, 0), textcoords='figure pixels')
    fig.canvas.draw()

    init_pos = ann.get_window_extent(fig.canvas.renderer)
    shift_val = 15
    ann.xyann = (shift_val, shift_val)
    fig.canvas.draw()
    post_pos = ann.get_window_extent(fig.canvas.renderer)

    for a, b in zip(init_pos.min, post_pos.min):
        assert a + shift_val == b

