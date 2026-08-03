from pathlib import Path


def test_path_intersect_path(phi):
    # test for the range of intersection angles
    eps_array = [1e-5, 1e-8, 1e-10, 1e-12]

    transform = transforms.Affine2D().rotate(np.deg2rad(phi))

    # a and b intersect at angle phi
    a = Path([(-2, 0), (2, 0)])
    b = transform.transform_path(a)
    assert a.intersects_path(b) and b.intersects_path(a)

    # a and b touch at angle phi at (0, 0)
    a = Path([(0, 0), (2, 0)])
    b = transform.transform_path(a)
    assert a.intersects_path(b) and b.intersects_path(a)

    # a and b are orthogonal and intersect at (0, 3)
    a = transform.transform_path(Path([(0, 1), (0, 3)]))
    b = transform.transform_path(Path([(1, 3), (0, 3)]))
    assert a.intersects_path(b) and b.intersects_path(a)

    # a and b are collinear and intersect at (0, 3)
    a = transform.transform_path(Path([(0, 1), (0, 3)]))
    b = transform.transform_path(Path([(0, 5), (0, 3)]))
    assert a.intersects_path(b) and b.intersects_path(a)

    # self-intersect
    assert a.intersects_path(a)

    # a contains b
    a = transform.transform_path(Path([(0, 0), (5, 5)]))
    b = transform.transform_path(Path([(1, 1), (3, 3)]))
    assert a.intersects_path(b) and b.intersects_path(a)

    # a and b are collinear but do not intersect
    a = transform.transform_path(Path([(0, 1), (0, 5)]))
    b = transform.transform_path(Path([(3, 0), (3, 3)]))
    assert not a.intersects_path(b) and not b.intersects_path(a)

    # a and b are on the same line but do not intersect
    a = transform.transform_path(Path([(0, 1), (0, 5)]))
    b = transform.transform_path(Path([(0, 6), (0, 7)]))
    assert not a.intersects_path(b) and not b.intersects_path(a)

    # Note: 1e-13 is the absolute tolerance error used for
    # `isclose` function from src/_path.h

    # a and b are parallel but do not touch
    for eps in eps_array:
        a = transform.transform_path(Path([(0, 1), (0, 5)]))
        b = transform.transform_path(Path([(0 + eps, 1), (0 + eps, 5)]))
        assert not a.intersects_path(b) and not b.intersects_path(a)

    # a and b are on the same line but do not intersect (really close)
    for eps in eps_array:
        a = transform.transform_path(Path([(0, 1), (0, 5)]))
        b = transform.transform_path(Path([(0, 5 + eps), (0, 7)]))
        assert not a.intersects_path(b) and not b.intersects_path(a)

    # a and b are on the same line and intersect (really close)
    for eps in eps_array:
        a = transform.transform_path(Path([(0, 1), (0, 5)]))
        b = transform.transform_path(Path([(0, 5 - eps), (0, 7)]))
        assert a.intersects_path(b) and b.intersects_path(a)

    # b is the same as a but with an extra point
    a = transform.transform_path(Path([(0, 1), (0, 5)]))
    b = transform.transform_path(Path([(0, 1), (0, 2), (0, 5)]))
    assert a.intersects_path(b) and b.intersects_path(a)

    # a and b are collinear but do not intersect
    a = transform.transform_path(Path([(1, -1), (0, -1)]))
    b = transform.transform_path(Path([(0, 1), (0.9, 1)]))
    assert not a.intersects_path(b) and not b.intersects_path(a)

    # a and b are collinear but do not intersect
    a = transform.transform_path(Path([(0., -5.), (1., -5.)]))
    b = transform.transform_path(Path([(1., 5.), (0., 5.)]))
    assert not a.intersects_path(b) and not b.intersects_path(a)

