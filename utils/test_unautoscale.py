
def test_unautoscale(axis, auto):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x = np.arange(100)
    y = np.linspace(-0.1, 0.1, 100)
    ax.scatter(x, y)

    get_autoscale_on = getattr(ax, f'get_autoscale{axis}_on')
    set_lim = getattr(ax, f'set_{axis}lim')
    get_lim = getattr(ax, f'get_{axis}lim')

    post_auto = get_autoscale_on() if auto is None else auto

    set_lim((-0.5, 0.5), auto=auto)
    assert post_auto == get_autoscale_on()
    fig.canvas.draw()
    np.testing.assert_array_equal(get_lim(), (-0.5, 0.5))


def test_unautoscale(axis, auto):
    fig, ax = plt.subplots()
    x = np.arange(100)
    y = np.linspace(-.1, .1, 100)
    ax.scatter(y, x)

    get_autoscale_on = getattr(ax, f'get_autoscale{axis}_on')
    set_lim = getattr(ax, f'set_{axis}lim')
    get_lim = getattr(ax, f'get_{axis}lim')

    post_auto = get_autoscale_on() if auto is None else auto

    set_lim((-0.5, 0.5), auto=auto)
    assert post_auto == get_autoscale_on()
    fig.canvas.draw()
    assert_array_equal(get_lim(), (-0.5, 0.5))

