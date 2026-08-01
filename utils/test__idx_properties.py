
def test_Idx_properties():
    i, a, b = symbols('i a b', integer=True)
    assert Idx(i).is_integer
    assert Idx(i).name == 'i'
    assert Idx(i + 2).name == 'i + 2'
    assert Idx('foo').name == 'foo'

