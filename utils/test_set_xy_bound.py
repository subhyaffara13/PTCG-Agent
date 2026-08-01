
def test_set_xy_bound():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xbound(2.0, 3.0)
    assert ax.get_xbound() == (2.0, 3.0)
    assert ax.get_xlim() == (2.0, 3.0)
    ax.set_xbound(upper=4.0)
    assert ax.get_xbound() == (2.0, 4.0)
    assert ax.get_xlim() == (2.0, 4.0)
    ax.set_xbound(lower=3.0)
    assert ax.get_xbound() == (3.0, 4.0)
    assert ax.get_xlim() == (3.0, 4.0)

    ax.set_ybound(2.0, 3.0)
    assert ax.get_ybound() == (2.0, 3.0)
    assert ax.get_ylim() == (2.0, 3.0)
    ax.set_ybound(upper=4.0)
    assert ax.get_ybound() == (2.0, 4.0)
    assert ax.get_ylim() == (2.0, 4.0)
    ax.set_ybound(lower=3.0)
    assert ax.get_ybound() == (3.0, 4.0)
    assert ax.get_ylim() == (3.0, 4.0)

