
def test_mec_rcparams():
    mpl.rcParams['lines.markeredgecolor'] = 'r'
    ln = mpl.lines.Line2D([1, 2], [1, 2])
    assert ln.get_markeredgecolor() == 'r'

