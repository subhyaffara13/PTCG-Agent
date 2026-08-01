
def test_deconstruct():
    expr     = Basic(S(1), S(2), S(3))
    expected = Compound(Basic, (1, 2, 3))
    assert deconstruct(expr) == expected

    assert deconstruct(1) == 1
    assert deconstruct(x) == x
    assert deconstruct(x, variables=(x,)) == Variable(x)
    assert deconstruct(Add(1, x, evaluate=False)) == Compound(Add, (1, x))
    assert deconstruct(Add(1, x, evaluate=False), variables=(x,)) == \
              Compound(Add, (1, Variable(x)))

