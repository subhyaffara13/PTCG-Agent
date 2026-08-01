
def test_annotationbbox_properties():
    ab = AnnotationBbox(DrawingArea(20, 20, 0, 0, clip=True), (0.5, 0.5),
                        xycoords='data')
    assert ab.xyann == (0.5, 0.5)  # xy if xybox not given
    assert ab.anncoords == 'data'  # xycoords if boxcoords not given

    ab = AnnotationBbox(DrawingArea(20, 20, 0, 0, clip=True), (0.5, 0.5),
                        xybox=(-0.2, 0.4), xycoords='data',
                        boxcoords='axes fraction')
    assert ab.xyann == (-0.2, 0.4)  # xybox if given
    assert ab.anncoords == 'axes fraction'  # boxcoords if given

