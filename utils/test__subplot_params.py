
def test_SubplotParams():
    s = gridspec.SubplotParams(.1, .1, .9, .9)
    assert s.left == 0.1

    s.reset()
    assert s.left == matplotlib.rcParams['figure.subplot.left']

    with pytest.raises(ValueError, match='left cannot be >= right'):
        s.update(left=s.right + .01)

    with pytest.raises(ValueError, match='bottom cannot be >= top'):
        s.update(bottom=s.top + .01)

    with pytest.raises(ValueError, match='left cannot be >= right'):
        gridspec.SubplotParams(.1, .1, .09, .9)

