
def test_old_docstring():
    a = (E + pi*I)*(E - pi*I)
    assert NS(a) == '17.2586605000200'
    assert a.n() == 17.25866050002001

