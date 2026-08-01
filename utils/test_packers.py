
def test_packers(align):
    # set the DPI to match points to make the math easier below
    fig = plt.figure(dpi=72)
    renderer = fig.canvas.get_renderer()

    x1, y1 = 10, 30
    x2, y2 = 20, 60
    r1 = DrawingArea(x1, y1)
    r2 = DrawingArea(x2, y2)

    # HPacker
    hpacker = HPacker(children=[r1, r2], align=align)
    hpacker.draw(renderer)
    bbox = hpacker.get_bbox(renderer)
    px, py = hpacker.get_offset(bbox, renderer)
    # width, height, xdescent, ydescent
    assert_allclose(bbox.bounds, (0, 0, x1 + x2, max(y1, y2)))
    # internal element placement
    if align in ("baseline", "left", "bottom"):
        y_height = 0
    elif align in ("right", "top"):
        y_height = y2 - y1
    elif align == "center":
        y_height = (y2 - y1) / 2
    # x-offsets, y-offsets
    assert_allclose([child.get_offset() for child in hpacker.get_children()],
                    [(px, py + y_height), (px + x1, py)])

    # VPacker
    vpacker = VPacker(children=[r1, r2], align=align)
    vpacker.draw(renderer)
    bbox = vpacker.get_bbox(renderer)
    px, py = vpacker.get_offset(bbox, renderer)
    # width, height, xdescent, ydescent
    assert_allclose(bbox.bounds, (0, -max(y1, y2), max(x1, x2), y1 + y2))
    # internal element placement
    if align in ("baseline", "left", "bottom"):
        x_height = 0
    elif align in ("right", "top"):
        x_height = x2 - x1
    elif align == "center":
        x_height = (x2 - x1) / 2
    # x-offsets, y-offsets
    assert_allclose([child.get_offset() for child in vpacker.get_children()],
                    [(px + x_height, py), (px, py - y2)])

