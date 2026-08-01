
def test_issue_24887():
    # Spherical pendulum
    g, l, m, c = symbols('g l m c')
    q1, q2, q3, u1, u2, u3 = dynamicsymbols('q1:4 u1:4')
    N = ReferenceFrame('N')
    A = ReferenceFrame('A')
    A.orient_body_fixed(N, (q1, q2, q3), 'zxy')
    N_w_A = A.ang_vel_in(N)
    # A.set_ang_vel(N, u1 * A.x + u2 * A.y + u3 * A.z)
    kdes = [N_w_A.dot(A.x) - u1, N_w_A.dot(A.y) - u2, N_w_A.dot(A.z) - u3]
    O = Point('O')
    O.set_vel(N, 0)
    Po = O.locatenew('Po', -l * A.y)
    Po.set_vel(A, 0)
    P = Particle('P', Po, m)
    kane = KanesMethod(N, [q1, q2, q3], [u1, u2, u3], kdes, bodies=[P],
                       forcelist=[(Po, -m * g * N.y)])
    kane.kanes_equations()
    expected_md = m * l ** 2 * Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
    expected_fd = Matrix([
        [l*m*(g*(sin(q1)*sin(q3) - sin(q2)*cos(q1)*cos(q3)) - l*u2*u3)],
        [0], [l*m*(-g*(sin(q1)*cos(q3) + sin(q2)*sin(q3)*cos(q1)) + l*u1*u2)]])
    assert find_dynamicsymbols(kane.forcing).issubset({q1, q2, q3, u1, u2, u3})
    assert simplify(kane.mass_matrix - expected_md) == zeros(3, 3)
    assert simplify(kane.forcing - expected_fd) == zeros(3, 1)

