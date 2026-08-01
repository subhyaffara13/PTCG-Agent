
def test_divider_append_axes():
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    axs = {
        "main": ax,
        "top": divider.append_axes("top", 1.2, pad=0.1, sharex=ax),
        "bottom": divider.append_axes("bottom", 1.2, pad=0.1, sharex=ax),
        "left": divider.append_axes("left", 1.2, pad=0.1, sharey=ax),
        "right": divider.append_axes("right", 1.2, pad=0.1, sharey=ax),
    }
    fig.canvas.draw()
    bboxes = {k: axs[k].get_window_extent() for k in axs}
    dpi = fig.dpi
    assert bboxes["top"].height == pytest.approx(1.2 * dpi)
    assert bboxes["bottom"].height == pytest.approx(1.2 * dpi)
    assert bboxes["left"].width == pytest.approx(1.2 * dpi)
    assert bboxes["right"].width == pytest.approx(1.2 * dpi)
    assert bboxes["top"].y0 - bboxes["main"].y1 == pytest.approx(0.1 * dpi)
    assert bboxes["main"].y0 - bboxes["bottom"].y1 == pytest.approx(0.1 * dpi)
    assert bboxes["main"].x0 - bboxes["left"].x1 == pytest.approx(0.1 * dpi)
    assert bboxes["right"].x0 - bboxes["main"].x1 == pytest.approx(0.1 * dpi)
    assert bboxes["left"].y0 == bboxes["main"].y0 == bboxes["right"].y0
    assert bboxes["left"].y1 == bboxes["main"].y1 == bboxes["right"].y1
    assert bboxes["top"].x0 == bboxes["main"].x0 == bboxes["bottom"].x0
    assert bboxes["top"].x1 == bboxes["main"].x1 == bboxes["bottom"].x1

