
def test_vector_var_in_dcm():

    N = ReferenceFrame('N')
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    u1, u2, u3, u4 = dynamicsymbols('u1 u2 u3 u4')

    v = u1 * u2 * A.x + u3 * N.y + u4**2 * N.z

    assert v.diff(u1, N, var_in_dcm=False) == u2 * A.x
    assert v.diff(u1, A, var_in_dcm=False) == u2 * A.x
    assert v.diff(u3, N, var_in_dcm=False) == N.y
    assert v.diff(u3, A, var_in_dcm=False) == N.y
    assert v.diff(u3, B, var_in_dcm=False) == N.y
    assert v.diff(u4, N, var_in_dcm=False) == 2 * u4 * N.z

    raises(ValueError, lambda: v.diff(u1, N))

