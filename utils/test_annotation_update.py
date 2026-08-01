
def test_annotation_update():
    fig, ax = plt.subplots(1, 1)
    an = ax.annotate('annotation', xy=(0.5, 0.5))
    extent1 = an.get_window_extent(fig.canvas.get_renderer())
    fig.tight_layout()
    extent2 = an.get_window_extent(fig.canvas.get_renderer())

    assert not np.allclose(extent1.get_points(), extent2.get_points(),
                           rtol=1e-6)

