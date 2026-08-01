
def test_title_location_shared(sharex):
    fig, axs = plt.subplots(2, 1, sharex=sharex)
    axs[0].set_title('A', pad=-40)
    axs[1].set_title('B', pad=-40)
    fig.draw_without_rendering()
    x, y1 = axs[0].title.get_position()
    x, y2 = axs[1].title.get_position()
    assert y1 == y2 == 1.0

