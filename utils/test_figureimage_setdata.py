
def test_figureimage_setdata():
    fig = plt.gcf()
    im = FigureImage(fig)
    z = np.arange(12, dtype=float).reshape((4, 3))
    im.set_data(z)
    z[0, 0] = 9.9
    assert im._A[0, 0] == 0, 'value changed'

