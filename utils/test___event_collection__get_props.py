
def test__EventCollection__get_props():
    _, coll, props = generate_EventCollection_plot()
    # check that the default segments have the correct coordinates
    check_segments(coll,
                   props['positions'],
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    # check that the default positions match the input positions
    np.testing.assert_array_equal(props['positions'], coll.get_positions())
    # check that the default orientation matches the input orientation
    assert props['orientation'] == coll.get_orientation()
    # check that the default orientation matches the input orientation
    assert coll.is_horizontal()
    # check that the default linelength matches the input linelength
    assert props['linelength'] == coll.get_linelength()
    # check that the default lineoffset matches the input lineoffset
    assert props['lineoffset'] == coll.get_lineoffset()
    # check that the default linestyle matches the input linestyle
    assert coll.get_linestyle() == [(0, None)]
    # check that the default color matches the input color
    for color in [coll.get_color(), *coll.get_colors()]:
        np.testing.assert_array_equal(color, props['color'])

