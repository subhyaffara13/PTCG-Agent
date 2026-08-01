
def test_transformedbbox_contains():
    bb = TransformedBbox(Bbox.unit(), Affine2D().rotate_deg(30))
    assert bb.contains(.8, .5)
    assert bb.contains(-.4, .85)
    assert not bb.contains(.9, .5)
    bb = TransformedBbox(Bbox.unit(), Affine2D().translate(.25, .5))
    assert bb.contains(1.25, 1.5)
    assert not bb.fully_contains(1.25, 1.5)
    assert not bb.fully_contains(.1, .1)

