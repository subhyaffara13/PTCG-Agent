
def test__EventCollection__set_color():
    splt, coll, _ = generate_EventCollection_plot()
    new_color = np.array([0, 1, 1, 1])
    coll.set_color(new_color)
    for color in [coll.get_color(), *coll.get_colors()]:
        np.testing.assert_array_equal(color, new_color)
    splt.set_title('EventCollection: set_color')

