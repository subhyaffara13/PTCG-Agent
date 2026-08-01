
def test_issue_25590():
    A = Symbol('A', commutative=False)
    B = Symbol('B', commutative=False)

    assert TR8(2*cos(x)*sin(x)*B*A) == sin(2*x)*B*A
    assert TR13(tan(2)*tan(3)*B*A) == (-tan(2)/tan(5) - tan(3)/tan(5) + 1)*B*A

    # XXX The result may not be optimal than
    # sin(2*x)*B*A + cos(x)**2 and may change in the future
    assert (2*cos(x)*sin(x)*B*A + cos(x)**2).simplify() == sin(2*x)*B*A + cos(2*x)/2 + S.One/2

