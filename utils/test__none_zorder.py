
def test_None_zorder():
    fig, ax = plt.subplots()
    ln, = ax.plot(range(5), zorder=None)
    assert ln.get_zorder() == mlines.Line2D.zorder
    ln.set_zorder(123456)
    assert ln.get_zorder() == 123456
    ln.set_zorder(None)
    assert ln.get_zorder() == mlines.Line2D.zorder

