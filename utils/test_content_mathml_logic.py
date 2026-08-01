
def test_content_mathml_logic():
    assert mathml(And(x, y)) == '<apply><and/><ci>x</ci><ci>y</ci></apply>'
    assert mathml(Or(x, y)) == '<apply><or/><ci>x</ci><ci>y</ci></apply>'
    assert mathml(Xor(x, y)) == '<apply><xor/><ci>x</ci><ci>y</ci></apply>'
    assert mathml(Implies(x, y)) == '<apply><implies/><ci>x</ci><ci>y</ci></apply>'
    assert mathml(Not(x)) == '<apply><not/><ci>x</ci></apply>'

