
def test_alignof():
    ax = alignof(x)
    assert ccode(ax) == 'alignof(x)'
    assert ax.func(*ax.args) == ax

