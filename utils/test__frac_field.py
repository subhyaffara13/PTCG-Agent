
def test_FracField():
    assert srepr(field("x", ZZ, lex)[0]) == "FracField((Symbol('x'),), ZZ, lex)"
    assert srepr(field("x,y", QQ, grlex)[0]) == "FracField((Symbol('x'), Symbol('y')), QQ, grlex)"
    assert srepr(field("x,y,z", ZZ["t"], lex)[0]) == "FracField((Symbol('x'), Symbol('y'), Symbol('z')), ZZ[t], lex)"


def test_FracField():
    assert str(field("x", ZZ, lex)[0]) == "Rational function field in x over ZZ with lex order"
    assert str(field("x,y", QQ, grlex)[0]) == "Rational function field in x, y over QQ with grlex order"
    assert str(field("x,y,z", ZZ["t"], lex)[0]) == "Rational function field in x, y, z over ZZ[t] with lex order"

