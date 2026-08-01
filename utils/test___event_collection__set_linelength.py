
def test__EventCollection__set_linelength():
    splt, coll, props = generate_EventCollection_plot()
    new_linelength = 15
    coll.set_linelength(new_linelength)
    assert new_linelength == coll.get_linelength()
    check_segments(coll,
                   props['positions'],
                   new_linelength,
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: set_linelength')
    splt.set_ylim(-20, 20)

