
def test__EventCollection__extend_positions():
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'],
                               props['extra_positions'][1:]])
    coll.extend_positions(props['extra_positions'][1:])
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: extend_positions')
    splt.set_xlim(-1, 90)

