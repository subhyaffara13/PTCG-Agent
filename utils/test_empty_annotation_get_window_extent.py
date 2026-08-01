
def test_empty_annotation_get_window_extent():
    figure = Figure(dpi=100)
    figure.set_figwidth(2.0)
    figure.set_figheight(2.0)
    renderer = RendererAgg(200, 200, 100)

    # Text annotation with arrow
    annotation = Annotation(
        '', xy=(0.0, 50.0), xytext=(0.0, 50.0), xycoords='figure pixels')
    annotation.set_figure(figure)
    annotation.draw(renderer)

    bbox = annotation.get_window_extent()
    points = bbox.get_points()

    assert points[0, 0] == 0.0
    assert points[1, 0] == 0.0
    assert points[1, 1] == 50.0
    assert points[0, 1] == 50.0

