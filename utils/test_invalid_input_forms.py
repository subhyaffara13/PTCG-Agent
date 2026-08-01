
def test_invalid_input_forms():
    fig, ax = plt.subplots()

    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle(1)
    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle([1, 2])

    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle('color', 'fish')

    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle('linewidth', 1)
    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle('linewidth', {1, 2})
    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle(linewidth=1, color='r')

    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle('foobar', [1, 2])
    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle(foobar=[1, 2])

    with pytest.raises((TypeError, ValueError)):
        ax.set_prop_cycle(cycler(foobar=[1, 2]))
    with pytest.raises(ValueError):
        ax.set_prop_cycle(cycler(color='rgb', c='cmy'))

