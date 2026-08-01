
def test__EventCollection__set_orientation():
    splt, coll, props = generate_EventCollection_plot()
    new_orientation = 'vertical'
    coll.set_orientation(new_orientation)
    assert new_orientation == coll.get_orientation()
    assert not coll.is_horizontal()
    check_segments(coll,
                   props['positions'],
                   props['linelength'],
                   props['lineoffset'],
                   new_orientation)
    splt.set_title('EventCollection: set_orientation')
    splt.set_ylim(-1, 22)
    splt.set_xlim(0, 2)

