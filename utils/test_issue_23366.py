
def test_issue_23366():
    u1 = dynamicsymbols('u1')
    N = ReferenceFrame('N')
    N_v_A = u1*N.x
    raises(VectorTypeError, lambda: N_v_A.diff(N, u1))

