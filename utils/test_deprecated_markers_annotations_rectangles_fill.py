
def test_deprecated_markers_annotations_rectangles_fill():
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    p = plot(sin(x), (x, -10, 10), show=False)
    with warns_deprecated_sympy():
        p.markers = [{"args":[[0, 1], [0, 1]], "marker": "*", "linestyle": "none"}]
    assert len(p._series) == 2
    with warns_deprecated_sympy():
        p.annotations = [{"text": "test", "xy": (0, 0)}]
    assert len(p._series) == 3
    with warns_deprecated_sympy():
        p.fill = {"x": [0, 1, 2, 3], "y1": [0, 1, 2, 3]}
    assert len(p._series) == 4
    with warns_deprecated_sympy():
        p.rectangles = [{"xy": (0, 0), "width": 5, "height": 1}]
    assert len(p._series) == 5

