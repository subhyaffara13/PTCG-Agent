
def test_issue_11413():
    from sympy.simplify.simplify import simplify
    v0 = Symbol('v0')
    v1 = Symbol('v1')
    v2 = Symbol('v2')
    V = Matrix([[v0],[v1],[v2]])
    U = V.normalized()
    assert U == Matrix([
    [v0/sqrt(Abs(v0)**2 + Abs(v1)**2 + Abs(v2)**2)],
    [v1/sqrt(Abs(v0)**2 + Abs(v1)**2 + Abs(v2)**2)],
    [v2/sqrt(Abs(v0)**2 + Abs(v1)**2 + Abs(v2)**2)]])
    U.norm = sqrt(v0**2/(v0**2 + v1**2 + v2**2) + v1**2/(v0**2 + v1**2 + v2**2) + v2**2/(v0**2 + v1**2 + v2**2))
    assert simplify(U.norm) == 1

