
def test_displaced_spine():
    with rc_context({'_internal.classic_mode': False}):
        fig, ax = plt.subplots(dpi=200, figsize=(6, 6))
        ax.set(xticklabels=[], yticklabels=[])
        ax.spines.bottom.set_position(('axes', -0.1))
        fig.canvas.draw()
        bbaxis, bbspines, bbax, bbtb = color_boxes(fig, ax)

    targets = [
        [150., 24., 930., 11.111111],
        [150.0, 1080.0, 930.0, 0.0],
        [150.0, 119.9999, 11.111, 960.0],
        [1068.8888, 119.9999, 11.111, 960.0]
    ]
    for target, bbspine in zip(targets, bbspines):
        targetbb = mtransforms.Bbox.from_bounds(*target)
        assert_allclose(bbspine.bounds, targetbb.bounds, atol=1e-2)

    target = [150.0, 119.99999999999997, 930.0, 960.0]
    targetbb = mtransforms.Bbox.from_bounds(*target)
    assert_allclose(bbax.bounds, targetbb.bounds, atol=1e-2)

    target = [150., 24., 930., 1056.]
    targetbb = mtransforms.Bbox.from_bounds(*target)
    assert_allclose(bbtb.bounds, targetbb.bounds, atol=1e-2)

