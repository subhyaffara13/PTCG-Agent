
def test_titlesetpos():
    # Test that title stays put if we set it manually
    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.8)
    ax2 = ax.twiny()
    ax.set_xlabel('Xlabel')
    ax2.set_xlabel('Xlabel2')
    ax.set_title('Title')
    pos = (0.5, 1.11)
    ax.title.set_position(pos)
    renderer = fig.canvas.get_renderer()
    ax._update_title_position(renderer)
    assert ax.title.get_position() == pos

