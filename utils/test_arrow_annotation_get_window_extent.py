
def test_arrow_annotation_get_window_extent():
    dpi = 100
    dots_per_point = dpi / 72
    figure = Figure(dpi=dpi)
    figure.set_figwidth(2.0)
    figure.set_figheight(2.0)
    renderer = RendererAgg(200, 200, 100)

    # Text annotation with arrow; arrow dimensions are in points
    annotation = Annotation(
        '', xy=(0.0, 50.0), xytext=(50.0, 50.0), xycoords='figure pixels',
        arrowprops={
            'facecolor': 'black', 'width': 8, 'headwidth': 10, 'shrink': 0.0})
    annotation.set_figure(figure)
    annotation.draw(renderer)

    bbox = annotation.get_window_extent()
    points = bbox.get_points()

    assert bbox.width == 50.0
    assert_almost_equal(bbox.height, 10.0 * dots_per_point)
    assert points[0, 0] == 0.0
    assert points[0, 1] == 50.0 - 5 * dots_per_point

