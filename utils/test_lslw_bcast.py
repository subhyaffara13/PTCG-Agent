
def test_lslw_bcast():
    col = mcollections.PathCollection([])
    col.set_linestyles(['-', '-'])
    col.set_linewidths([1, 2, 3])

    assert col.get_linestyles() == [(0, None)] * 6
    assert col.get_linewidths() == [1, 2, 3] * 2

    col.set_linestyles(['-', '-', '-'])
    assert col.get_linestyles() == [(0, None)] * 3
    assert (col.get_linewidths() == [1, 2, 3]).all()

