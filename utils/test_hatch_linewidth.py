
def test_hatch_linewidth(fig_test, fig_ref):
    ax_test = fig_test.add_subplot()
    ax_ref = fig_ref.add_subplot()

    lw = 2.0

    polygons = [
        [(0.1, 0.1), (0.1, 0.4), (0.4, 0.4), (0.4, 0.1)],
        [(0.6, 0.6), (0.6, 0.9), (0.9, 0.9), (0.9, 0.6)],
    ]
    ref = PolyCollection(polygons, hatch="x")
    ref.set_hatch_linewidth(lw)

    with mpl.rc_context({"hatch.linewidth": lw}):
        test = PolyCollection(polygons, hatch="x")

    ax_ref.add_collection(ref)
    ax_test.add_collection(test)

    assert test.get_hatch_linewidth() == ref.get_hatch_linewidth() == lw

