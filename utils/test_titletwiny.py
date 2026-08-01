
def test_titletwiny():
    plt.style.use('mpl20')
    fig, ax = plt.subplots(dpi=72)
    ax2 = ax.twiny()
    xlabel2 = ax2.set_xlabel('Xlabel2')
    title = ax.set_title('Title')
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    # ------- Test that title is put above Xlabel2 (Xlabel2 at top) ----------
    bbox_y0_title = title.get_window_extent(renderer).y0  # bottom of title
    bbox_y1_xlabel2 = xlabel2.get_window_extent(renderer).y1  # top of xlabel2
    y_diff = bbox_y0_title - bbox_y1_xlabel2
    assert y_diff >= 3

