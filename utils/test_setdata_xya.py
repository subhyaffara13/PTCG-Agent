
def test_setdata_xya(image_cls, x, y, a):
    ax = plt.gca()
    im = image_cls(ax)
    im.set_data(x, y, a)
    x[0] = y[0] = a[0, 0] = 9.9
    assert im._A[0, 0] == im._Ax[0] == im._Ay[0] == 0, 'value changed'
    im.set_data(x, y, a.reshape((*a.shape, -1)))  # Just a smoketest.

