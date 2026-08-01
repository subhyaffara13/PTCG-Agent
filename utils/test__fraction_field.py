
def test_FractionField():
    assert srepr(QQ.frac_field(x)) == \
        "FractionField(FracField((Symbol('x'),), QQ, lex))"
    assert srepr(QQ.frac_field(x, y, order=grlex)) == \
        "FractionField(FracField((Symbol('x'), Symbol('y')), QQ, grlex))"

