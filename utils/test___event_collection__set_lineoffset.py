
def test__EventCollection__set_lineoffset():
    splt, coll, props = generate_EventCollection_plot()
    new_lineoffset = -5.
    coll.set_lineoffset(new_lineoffset)
    assert new_lineoffset == coll.get_lineoffset()
    check_segments(coll,
                   props['positions'],
                   props['linelength'],
                   new_lineoffset,
                   props['orientation'])
    splt.set_title('EventCollection: set_lineoffset')
    splt.set_ylim(-6, -4)

