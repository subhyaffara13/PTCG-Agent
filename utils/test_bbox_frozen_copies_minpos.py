
def test_bbox_frozen_copies_minpos():
    bbox = mtransforms.Bbox.from_extents(0.0, 0.0, 1.0, 1.0, minpos=1.0)
    frozen = bbox.frozen()
    assert_array_equal(frozen.minpos, bbox.minpos)

