
def test_exact_extents(path, extents):
    # notice that if we just looked at the control points to get the bounding
    # box of each curve, we would get the wrong answers. For example, for
    # hard_curve = Path([[0, 0], [1, 0], [1, 1], [0, 1]],
    #                   [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    # we would get that the extents area (0, 0, 1, 1). This code takes into
    # account the curved part of the path, which does not typically extend all
    # the way out to the control points.
    # Note that counterintuitively, path.get_extents() returns a Bbox, so we
    # have to get that Bbox's `.extents`.
    assert np.all(path.get_extents().extents == extents)

