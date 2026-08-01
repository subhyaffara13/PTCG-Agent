
def test_subfigure_remove():
    fig = plt.figure()
    sfs = fig.subfigures(2, 2)
    sfs[1, 1].subplots()
    sfs[1, 1].remove()
    assert len(fig.subfigs) == 3

