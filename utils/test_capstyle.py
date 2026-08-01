
def test_capstyle():
    col = mcollections.PathCollection([])
    assert col.get_capstyle() is None
    col = mcollections.PathCollection([], capstyle='round')
    assert col.get_capstyle() == 'round'
    col.set_capstyle('butt')
    assert col.get_capstyle() == 'butt'

