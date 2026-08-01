
def test_Subs_printing():
    assert str(Subs(x, (x,), (1,))) == 'Subs(x, x, 1)'
    assert str(Subs(x + y, (x, y), (1, 2))) == 'Subs(x + y, (x, y), (1, 2))'

