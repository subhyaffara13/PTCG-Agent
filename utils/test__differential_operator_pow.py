
def test_DifferentialOperatorPow():
    x = symbols('x', integer=True)
    R, _ = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')
    do = DifferentialOperator([x**2, R.base.zero, R.base.zero], R)
    a = DifferentialOperator([R.base.one], R)
    for n in range(10):
        assert a == do**n
        a *= do

