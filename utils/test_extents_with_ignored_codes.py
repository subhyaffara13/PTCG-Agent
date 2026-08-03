from pathlib import Path


def test_extents_with_ignored_codes(ignored_code):
    # Check that STOP and CLOSEPOLY points are ignored when calculating extents
    # of a path with only straight lines
    path = Path([[0, 0],
                 [1, 1],
                 [2, 2]], [Path.MOVETO, Path.MOVETO, ignored_code])
    assert np.all(path.get_extents().extents == (0., 0., 1., 1.))

