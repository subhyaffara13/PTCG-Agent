
def test_normal_axes():
    with rc_context({'_internal.classic_mode': False}):
        fig, ax = plt.subplots(dpi=200, figsize=(6, 6))
        fig.canvas.draw()
        plt.close(fig)
        bbaxis, bbspines, bbax, bbtb = color_boxes(fig, ax)

    # test the axis bboxes
    target = [
        [124.0, 75.56, 982.0, 33.33],
        [86.89, 99.33, 52.0, 993.33],
    ]
    for nn, b in enumerate(bbaxis):
        targetbb = mtransforms.Bbox.from_bounds(*target[nn])
        assert_array_almost_equal(b.bounds, targetbb.bounds, decimal=1)

    target = [
        [150.0, 119.999, 930.0, 11.111],
        [150.0, 1080.0, 930.0, 0.0],
        [150.0, 119.9999, 11.111, 960.0],
        [1068.8888, 119.9999, 11.111, 960.0]
    ]
    for nn, b in enumerate(bbspines):
        targetbb = mtransforms.Bbox.from_bounds(*target[nn])
        assert_array_almost_equal(b.bounds, targetbb.bounds, decimal=2)

    target = [150.0, 119.99999999999997, 930.0, 960.0]
    targetbb = mtransforms.Bbox.from_bounds(*target)
    assert_array_almost_equal(bbax.bounds, targetbb.bounds, decimal=2)

    target = [86.89, 75.56, 1019.11, 1017.11]
    targetbb = mtransforms.Bbox.from_bounds(*target)
    assert_array_almost_equal(bbtb.bounds, targetbb.bounds, decimal=1)

    # test that get_position roundtrips to get_window_extent
    axbb = ax.get_position().transformed(fig.transFigure).bounds
    assert_array_almost_equal(axbb, ax.get_window_extent().bounds, decimal=2)

