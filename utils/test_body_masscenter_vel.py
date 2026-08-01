
def test_body_masscenter_vel():
    with warns_deprecated_sympy():
        A = Body('A')
    N = ReferenceFrame('N')
    with warns_deprecated_sympy():
        B = Body('B', frame=N)
    A.masscenter.set_vel(N, N.z)
    assert A.masscenter_vel(B) == N.z
    assert A.masscenter_vel(N) == N.z

