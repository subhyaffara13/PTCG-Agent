
def test_autoscale():
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    assert ax.get_zscale() == 'linear'
    ax._view_margin = 0
    ax.margins(x=0, y=.1, z=.2)
    ax.plot([0, 1], [0, 1], [0, 1])
    assert ax.get_w_lims() == (0, 1, -.1, 1.1, -.2, 1.2)
    ax.autoscale(False)
    ax.set_autoscalez_on(True)
    ax.plot([0, 2], [0, 2], [0, 2])
    assert ax.get_w_lims() == (0, 1, -.1, 1.1, -.4, 2.4)
    ax.autoscale(axis='x')
    ax.plot([0, 2], [0, 2], [0, 2])
    assert ax.get_w_lims() == (0, 2, -.1, 1.1, -.4, 2.4)

