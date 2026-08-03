from pathlib import Path


def test_simplify_closepoly():
    # The values of the vertices in a CLOSEPOLY should always be ignored,
    # in favor of the most recent MOVETO's vertex values
    paths = [Path([(1, 1), (2, 1), (2, 2), (np.nan, np.nan)],
                  [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]),
             Path([(1, 1), (2, 1), (2, 2), (40, 50)],
                  [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])]
    expected_path = Path([(1, 1), (2, 1), (2, 2), (1, 1), (1, 1), (0, 0)],
                         [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                          Path.LINETO, Path.STOP])

    for path in paths:
        simplified_path = path.cleaned(simplify=True)
        assert_array_equal(expected_path.vertices, simplified_path.vertices)
        assert_array_equal(expected_path.codes, simplified_path.codes)

    # test that a compound path also works
    path = Path([(1, 1), (2, 1), (2, 2), (np.nan, np.nan),
                 (-1, 0), (-2, 0), (-2, 1), (np.nan, np.nan)],
                [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY,
                 Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    expected_path = Path([(1, 1), (2, 1), (2, 2), (1, 1),
                          (-1, 0), (-2, 0), (-2, 1), (-1, 0), (-1, 0), (0, 0)],
                         [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                          Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                          Path.LINETO, Path.STOP])

    simplified_path = path.cleaned(simplify=True)
    assert_array_equal(expected_path.vertices, simplified_path.vertices)
    assert_array_equal(expected_path.codes, simplified_path.codes)

    # test for a path with an invalid MOVETO
    # CLOSEPOLY with an invalid MOVETO should be ignored
    path = Path([(1, 0), (1, -1), (2, -1),
                 (np.nan, np.nan), (-1, -1), (-2, 1), (-1, 1),
                 (2, 2), (0, -1)],
                [Path.MOVETO, Path.LINETO, Path.LINETO,
                 Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                 Path.CLOSEPOLY, Path.LINETO])
    expected_path = Path([(1, 0), (1, -1), (2, -1),
                          (np.nan, np.nan), (-1, -1), (-2, 1), (-1, 1),
                          (0, -1), (0, -1), (0, 0)],
                         [Path.MOVETO, Path.LINETO, Path.LINETO,
                          Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                          Path.LINETO, Path.LINETO, Path.STOP])

    simplified_path = path.cleaned(simplify=True)
    assert_array_equal(expected_path.vertices, simplified_path.vertices)
    assert_array_equal(expected_path.codes, simplified_path.codes)

