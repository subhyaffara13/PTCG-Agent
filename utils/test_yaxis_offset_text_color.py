
def test_yaxis_offsetText_color():
    plt.rcParams['ytick.labelcolor'] = 'green'
    ax = plt.axes()
    assert ax.yaxis.offsetText.get_color() == 'green'

    plt.rcParams['ytick.color'] = 'red'
    plt.rcParams['ytick.labelcolor'] = 'inherit'
    ax = plt.axes()
    assert ax.yaxis.offsetText.get_color() == 'red'

