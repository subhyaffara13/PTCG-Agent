
def test__EventCollection__set_prop():
    for prop, value, expected in [
            ('linestyle', 'dashed', [(0, [7.4, 3.2])]),
            # Dashes are scaled by linewidth.
            ('linestyle', (0, (3.7, 1.6)), [(0, [7.4, 3.2])]),
            ('linewidth', 5, 5),
    ]:
        splt, coll, _ = generate_EventCollection_plot()
        coll.set(**{prop: value})
        assert plt.getp(coll, prop) == expected
        splt.set_title(f'EventCollection: set_{prop}')

