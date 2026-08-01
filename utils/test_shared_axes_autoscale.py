
def test_shared_axes_autoscale():
    l = np.arange(-80, 90, 40)
    t = np.random.random_sample((l.size, l.size))

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)

    ax1.set_xlim(-1000, 1000)
    ax1.set_ylim(-1000, 1000)
    ax1.contour(l, l, t)

    ax2.contour(l, l, t)
    assert not ax1.get_autoscalex_on() and not ax2.get_autoscalex_on()
    assert not ax1.get_autoscaley_on() and not ax2.get_autoscaley_on()
    assert ax1.get_xlim() == ax2.get_xlim() == (-1000, 1000)
    assert ax1.get_ylim() == ax2.get_ylim() == (-1000, 1000)

