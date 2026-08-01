
def test_bbox_aspect_axes_init():
    # Test that box_aspect can be given to axes init and produces
    # all equal square axes.
    fig, axs = plt.subplots(2, 3, subplot_kw=dict(box_aspect=1),
                            constrained_layout=True)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    sizes = []
    for ax in axs.flat:
        bb = ax.get_window_extent(renderer)
        sizes.extend([bb.width, bb.height])

    assert_allclose(sizes, sizes[0])

