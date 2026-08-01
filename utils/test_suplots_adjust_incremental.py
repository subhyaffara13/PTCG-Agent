
def test_suplots_adjust_incremental():
    fig = plt.figure()
    fig.subplots_adjust(left=0)
    fig.subplots_adjust(right=1)
    assert fig.subplotpars.left == 0
    assert fig.subplotpars.right == 1

