
def test_relim_visible_only():
    x1 = (0., 10.)
    y1 = (0., 10.)
    x2 = (-10., 20.)
    y2 = (-10., 30.)

    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot()
    ax.plot(x1, y1)
    assert ax.get_xlim() == x1
    assert ax.get_ylim() == y1
    line, = ax.plot(x2, y2)
    assert ax.get_xlim() == x2
    assert ax.get_ylim() == y2
    line.set_visible(False)
    assert ax.get_xlim() == x2
    assert ax.get_ylim() == y2

    ax.relim(visible_only=True)
    ax.autoscale_view()

    assert ax.get_xlim() == x1
    assert ax.get_ylim() == y1

