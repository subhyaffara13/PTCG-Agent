
def test_transpose_power():
    from sympy.matrices.expressions.transpose import Transpose as TP

    assert (C*D).T**5 == ((C*D)**5).T == (D.T * C.T)**5
    assert ((C*D).T**5).T == (C*D)**5

    assert (C.T.I.T)**7 == C**-7
    assert (C.T**l).T**k == C**(l*k)

    assert ((E.T * A.T)**5).T == (A*E)**5
    assert ((A*E).T**5).T**7 == (A*E)**35
    assert TP(TP(C**2 * D**3)**5).doit() == (C**2 * D**3)**5

    assert ((D*C)**-5).T**-5 == ((D*C)**25).T
    assert (((D*C)**l).T**k).T == (D*C)**(l*k)

