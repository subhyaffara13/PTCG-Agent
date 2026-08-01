
def test_body_ang_vel():
    with warns_deprecated_sympy():
        A = Body('A')
    N = ReferenceFrame('N')
    with warns_deprecated_sympy():
        B = Body('B', frame=N)
    A.frame.set_ang_vel(N, N.y)
    assert A.ang_vel_in(B) == N.y
    assert B.ang_vel_in(A) == -N.y
    assert A.ang_vel_in(N) == N.y

