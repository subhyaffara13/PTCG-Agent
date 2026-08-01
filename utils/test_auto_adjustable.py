
def test_auto_adjustable():
    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1))
    pad = 0.1
    make_axes_area_auto_adjustable(ax, pad=pad)
    fig.canvas.draw()
    tbb = ax.get_tightbbox()
    assert tbb.x0 == pytest.approx(pad * fig.dpi)
    assert tbb.x1 == pytest.approx(fig.bbox.width - pad * fig.dpi)
    assert tbb.y0 == pytest.approx(pad * fig.dpi)
    assert tbb.y1 == pytest.approx(fig.bbox.height - pad * fig.dpi)

