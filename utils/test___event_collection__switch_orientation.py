
def test__EventCollection__switch_orientation():
    splt, coll, props = generate_EventCollection_plot()
    new_orientation = 'vertical'
    coll.switch_orientation()
    assert new_orientation == coll.get_orientation()
    assert not coll.is_horizontal()
    new_positions = coll.get_positions()
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'], new_orientation)
    splt.set_title('EventCollection: switch_orientation')
    splt.set_ylim(-1, 22)
    splt.set_xlim(0, 2)

