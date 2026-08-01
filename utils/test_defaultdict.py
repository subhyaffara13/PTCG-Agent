
def test_defaultdict():
    assert next(unify(Variable('x'), 'foo')) == {Variable('x'): 'foo'}

