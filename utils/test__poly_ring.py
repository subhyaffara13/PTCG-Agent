
def test_PolyRing():
    assert srepr(ring("x", ZZ, lex)[0]) == "PolyRing((Symbol('x'),), ZZ, lex)"
    assert srepr(ring("x,y", QQ, grlex)[0]) == "PolyRing((Symbol('x'), Symbol('y')), QQ, grlex)"
    assert srepr(ring("x,y,z", ZZ["t"], lex)[0]) == "PolyRing((Symbol('x'), Symbol('y'), Symbol('z')), ZZ[t], lex)"


def test_PolyRing():
    assert str(ring("x", ZZ, lex)[0]) == "Polynomial ring in x over ZZ with lex order"
    assert str(ring("x,y", QQ, grlex)[0]) == "Polynomial ring in x, y over QQ with grlex order"
    assert str(ring("x,y,z", ZZ["t"], lex)[0]) == "Polynomial ring in x, y, z over ZZ[t] with lex order"

