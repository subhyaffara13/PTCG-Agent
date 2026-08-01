
def test_location_event_position_twin():
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 10), ylim=(0, 20))
    assert ax.format_coord(5., 5.) == "(x, y) = (5.00, 5.00)"
    ax.twinx().set(ylim=(0, 40))
    assert ax.format_coord(5., 5.) == "(x, y) = (5.00, 5.00) | (5.00, 10.0)"
    ax.twiny().set(xlim=(0, 5))
    assert (ax.format_coord(5., 5.)
            == "(x, y) = (5.00, 5.00) | (5.00, 10.0) | (2.50, 5.00)")

