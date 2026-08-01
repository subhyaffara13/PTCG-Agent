
def test_arrowprops_copied():
    da = DrawingArea(20, 20, 0, 0, clip=True)
    arrowprops = {"arrowstyle": "->", "relpos": (.3, .7)}
    ab = AnnotationBbox(da, [.5, .5], xybox=(-0.2, 0.5), xycoords='data',
                        boxcoords="axes fraction", box_alignment=(0., .5),
                        arrowprops=arrowprops)
    assert ab.arrowprops is not ab
    assert arrowprops["relpos"] == (.3, .7)

