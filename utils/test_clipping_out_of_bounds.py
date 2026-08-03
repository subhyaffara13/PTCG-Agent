from pathlib import Path


def test_clipping_out_of_bounds():
    # Should work on a Path *without* codes.
    path = Path([(0, 0), (1, 2), (2, 1)])
    simplified = path.cleaned(clip=(10, 10, 20, 20))
    assert_array_equal(simplified.vertices, [(0, 0)])
    assert simplified.codes == [Path.STOP]

    # Should work on a Path *with* codes, and no curves.
    path = Path([(0, 0), (1, 2), (2, 1)],
                [Path.MOVETO, Path.LINETO, Path.LINETO])
    simplified = path.cleaned(clip=(10, 10, 20, 20))
    assert_array_equal(simplified.vertices, [(0, 0)])
    assert simplified.codes == [Path.STOP]

    # A Path with curves does not do any clipping yet.
    path = Path([(0, 0), (1, 2), (2, 3)],
                [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    simplified = path.cleaned()
    simplified_clipped = path.cleaned(clip=(10, 10, 20, 20))
    assert_array_equal(simplified.vertices, simplified_clipped.vertices)
    assert_array_equal(simplified.codes, simplified_clipped.codes)

