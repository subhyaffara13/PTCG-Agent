
def test_rc_axes_label_formatting():
    mpl.rcParams['axes.labelcolor'] = 'red'
    mpl.rcParams['axes.labelsize'] = 20
    mpl.rcParams['axes.labelweight'] = 'bold'

    ax = plt.axes()
    assert ax.xaxis.label.get_color() == 'red'
    assert ax.xaxis.label.get_fontsize() == 20
    assert ax.xaxis.label.get_fontweight() == 'bold'

