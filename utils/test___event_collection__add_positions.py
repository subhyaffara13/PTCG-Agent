
def test__EventCollection__add_positions():
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'],
                               props['extra_positions'][0]])
    coll.switch_orientation()  # Test adding in the vertical orientation, too.
    coll.add_positions(props['extra_positions'][0])
    coll.switch_orientation()
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: add_positions')
    splt.set_xlim(-1, 35)

