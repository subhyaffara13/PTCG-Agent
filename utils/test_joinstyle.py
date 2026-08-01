
def test_joinstyle():
    col = mcollections.PathCollection([])
    assert col.get_joinstyle() is None
    col = mcollections.PathCollection([], joinstyle='round')
    assert col.get_joinstyle() == 'round'
    col.set_joinstyle('miter')
    assert col.get_joinstyle() == 'miter'

