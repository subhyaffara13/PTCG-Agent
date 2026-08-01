
def test_bbox_intersection():
    bbox_from_ext = mtransforms.Bbox.from_extents
    inter = mtransforms.Bbox.intersection

    r1 = bbox_from_ext(0, 0, 1, 1)
    r2 = bbox_from_ext(0.5, 0.5, 1.5, 1.5)
    r3 = bbox_from_ext(0.5, 0, 0.75, 0.75)
    r4 = bbox_from_ext(0.5, 1.5, 1, 2.5)
    r5 = bbox_from_ext(1, 1, 2, 2)

    # self intersection -> no change
    assert_bbox_eq(inter(r1, r1), r1)
    # simple intersection
    assert_bbox_eq(inter(r1, r2), bbox_from_ext(0.5, 0.5, 1, 1))
    # r3 contains r2
    assert_bbox_eq(inter(r1, r3), r3)
    # no intersection
    assert inter(r1, r4) is None
    # single point
    assert_bbox_eq(inter(r1, r5), bbox_from_ext(1, 1, 1, 1))

