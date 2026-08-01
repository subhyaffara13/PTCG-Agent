
def test_annotationbbox_extents(extent_kind):
    plt.rcParams.update(plt.rcParamsDefault)
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

    ax.axis([0, 1, 0, 1])

    an1 = ax.annotate("Annotation", xy=(.9, .9), xytext=(1.1, 1.1),
                      arrowprops=dict(arrowstyle="->"), clip_on=False,
                      va="baseline", ha="left")

    da = DrawingArea(20, 20, 0, 0, clip=True)
    p = mpatches.Circle((-10, 30), 32)
    da.add_artist(p)

    ab3 = AnnotationBbox(da, [.5, .5], xybox=(-0.2, 0.5), xycoords='data',
                         boxcoords="axes fraction", box_alignment=(0., .5),
                         arrowprops=dict(arrowstyle="->"))
    ax.add_artist(ab3)

    im = OffsetImage(np.random.rand(10, 10), zoom=3)
    im.image.axes = ax
    ab6 = AnnotationBbox(im, (0.5, -.3), xybox=(0, 75),
                         xycoords='axes fraction',
                         boxcoords="offset points", pad=0.3,
                         arrowprops=dict(arrowstyle="->"))
    ax.add_artist(ab6)

    # Test Annotation
    bb1 = getattr(an1, f"get_{extent_kind}")()

    target1 = [332.9, 242.8, 467.0, 298.9]
    assert_allclose(bb1.extents, target1, atol=2)

    # Test AnnotationBbox
    bb3 = getattr(ab3, f"get_{extent_kind}")()

    target3 = [-17.6, 129.0, 200.7, 167.9]
    assert_allclose(bb3.extents, target3, atol=2)

    bb6 = getattr(ab6, f"get_{extent_kind}")()

    target6 = [180.0, -32.0, 230.0, 92.9]
    assert_allclose(bb6.extents, target6, atol=2)

    # Test bbox_inches='tight'
    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches='tight')
    buf.seek(0)
    shape = plt.imread(buf).shape
    targetshape = (350, 504, 4)
    assert_allclose(shape, targetshape, atol=2)

    # Simple smoke test for tight_layout, to make sure it does not error out.
    fig.canvas.draw()
    fig.tight_layout()
    fig.canvas.draw()

