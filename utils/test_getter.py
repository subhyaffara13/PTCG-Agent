
def test_getter():
    assert getter(0)('Alice') == 'A'
    assert getter([0])('Alice') == ('A',)
    assert getter([])('Alice') == ()

