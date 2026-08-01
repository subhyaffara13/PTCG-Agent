
def test_issue_8263():
    F, G = symbols('F, G', commutative=False, cls=Function)
    x, y = symbols('x, y')
    expr, dummies, _ = _mask_nc(F(x)*G(y) - G(y)*F(x))
    for v in dummies.values():
        assert not v.is_commutative
    assert not expr.is_zero

