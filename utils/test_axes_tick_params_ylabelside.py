
def test_axes_tick_params_ylabelside():
    # Tests fix for issue 10267
    ax = plt.subplot()
    ax.tick_params(labelleft=False, labelright=True,
                   which='major')
    ax.tick_params(labelleft=False, labelright=True,
                   which='minor')
    # expects left false, right true
    assert ax.yaxis.majorTicks[0].label1.get_visible() is False
    assert ax.yaxis.majorTicks[0].label2.get_visible() is True
    assert ax.yaxis.minorTicks[0].label1.get_visible() is False
    assert ax.yaxis.minorTicks[0].label2.get_visible() is True

