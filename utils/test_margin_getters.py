
def test_margin_getters():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.margins(0.1, 0.2, 0.3)
    assert ax.get_xmargin() == 0.1
    assert ax.get_ymargin() == 0.2
    assert ax.get_zmargin() == 0.3


def test_margin_getters():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.margins(0.2, 0.3)
    assert ax.get_xmargin() == 0.2
    assert ax.get_ymargin() == 0.3

