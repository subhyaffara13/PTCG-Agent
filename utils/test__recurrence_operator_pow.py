
def test_RecurrenceOperatorPow():
    n = symbols('n', integer=True)
    R, _ = RecurrenceOperators(QQ.old_poly_ring(n), 'Sn')
    rr = RecurrenceOperator([n**2, 0, 0], R)
    a = RecurrenceOperator([R.base.one], R)
    for m in range(10):
        assert a == rr**m
        a *= rr

