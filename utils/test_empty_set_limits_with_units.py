
def test_empty_set_limits_with_units(quantity_converter):
    # Register the class
    munits.registry[Quantity] = quantity_converter

    fig, ax = plt.subplots()
    ax.set_xlim(Quantity(-1, 'meters'), Quantity(6, 'meters'))
    ax.set_ylim(Quantity(-1, 'hours'), Quantity(16, 'hours'))

