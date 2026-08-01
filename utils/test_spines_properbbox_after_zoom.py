
def test_spines_properbbox_after_zoom():
    fig, ax = plt.subplots()
    bb = ax.spines.bottom.get_window_extent(fig.canvas.get_renderer())
    # this is what zoom calls:
    ax._set_view_from_bbox((320, 320, 500, 500), 'in',
                           None, False, False)
    bb2 = ax.spines.bottom.get_window_extent(fig.canvas.get_renderer())
    np.testing.assert_allclose(bb.get_points(), bb2.get_points(), rtol=1e-6)

