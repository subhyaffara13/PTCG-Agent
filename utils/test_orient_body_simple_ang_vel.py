
def test_orient_body_simple_ang_vel():
    """This test ensures that the simplest form of that linear system solution
    is returned, thus the == for the expression comparison."""

    psi, theta, phi = dynamicsymbols('psi, theta, varphi')
    t = dynamicsymbols._t
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    B.orient_body_fixed(A, (psi, theta, phi), 'ZXZ')
    A_w_B = B.ang_vel_in(A)
    assert A_w_B.args[0][1] == B
    assert A_w_B.args[0][0][0] == (sin(theta)*sin(phi)*psi.diff(t) +
                                   cos(phi)*theta.diff(t))
    assert A_w_B.args[0][0][1] == (sin(theta)*cos(phi)*psi.diff(t) -
                                   sin(phi)*theta.diff(t))
    assert A_w_B.args[0][0][2] == cos(theta)*psi.diff(t) + phi.diff(t)

