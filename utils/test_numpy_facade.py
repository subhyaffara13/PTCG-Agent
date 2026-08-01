
def test_numpy_facade(quantity_converter):
    # use former defaults to match existing baseline image
    plt.rcParams['axes.formatter.limits'] = -7, 7

    # Register the class
    munits.registry[Quantity] = quantity_converter

    # Simple test
    y = Quantity(np.linspace(0, 30), 'miles')
    x = Quantity(np.linspace(0, 5), 'hours')

    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.15)  # Make space for label
    ax.plot(x, y, 'tab:blue')
    ax.axhline(Quantity(26400, 'feet'), color='tab:red')
    ax.axvline(Quantity(120, 'minutes'), color='tab:green')
    ax.yaxis.set_units('inches')
    ax.xaxis.set_units('seconds')

    assert quantity_converter.convert.called
    assert quantity_converter.axisinfo.called
    assert quantity_converter.default_units.called

