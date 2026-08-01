
def test_ft2font_get_path():
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    font.set_size(12, 72)
    vertices, codes = font.get_path()
    assert vertices.shape == (0, 2)
    assert codes.shape == (0, )
    font.load_char(ord('M'))
    vertices, codes = font.get_path()
    expected_vertices = np.array([
        (0.843750, 9.000000), (2.609375, 9.000000),  # Top left.
        (4.906250, 2.875000),  # Top of midpoint.
        (7.218750, 9.000000), (8.968750, 9.000000),  # Top right.
        (8.968750, 0.000000), (7.843750, 0.000000),  # Bottom right.
        (7.843750, 7.906250),  # Point under top right.
        (5.531250, 1.734375), (4.296875, 1.734375),  # Bar under midpoint.
        (1.984375, 7.906250),  # Point under top left.
        (1.984375, 0.000000), (0.843750, 0.000000),  # Bottom left.
        (0.843750, 9.000000),  # Back to top left corner.
        (0.000000, 0.000000),
    ])
    np.testing.assert_array_equal(vertices, expected_vertices)
    expected_codes = np.full(expected_vertices.shape[0], mpath.Path.LINETO,
                             dtype=mpath.Path.code_type)
    expected_codes[0] = mpath.Path.MOVETO
    expected_codes[-1] = mpath.Path.CLOSEPOLY
    np.testing.assert_array_equal(codes, expected_codes)

