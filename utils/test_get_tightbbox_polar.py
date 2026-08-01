
def test_get_tightbbox_polar():
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    fig.canvas.draw()
    bb = ax.get_tightbbox(fig.canvas.get_renderer())
    assert_allclose(
        bb.extents, [108.27778, 29.1111, 539.7222, 450.8889], rtol=1e-03)

