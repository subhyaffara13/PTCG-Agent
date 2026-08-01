
def test_input_format():
    raises(TypeError, lambda: diophantine(sin(x)))
    raises(TypeError, lambda: diophantine(x/pi - 3))


def test_input_format():
    # 1 dof problem from test_one_dof
    q, u = dynamicsymbols('q u')
    qd, ud = dynamicsymbols('q u', 1)
    m, c, k = symbols('m c k')
    N = ReferenceFrame('N')
    P = Point('P')
    P.set_vel(N, u * N.x)

    kd = [qd - u]
    FL = [(P, (-k * q - c * u) * N.x)]
    pa = Particle('pa', P, m)
    BL = [pa]

    KM = KanesMethod(N, [q], [u], kd)
    # test for input format kane.kanes_equations((body1, body2, particle1))
    assert KM.kanes_equations(BL)[0] == Matrix([0])
    # test for input format kane.kanes_equations(bodies=(body1, body 2), loads=(load1,load2))
    assert KM.kanes_equations(bodies=BL, loads=None)[0] == Matrix([0])
    # test for input format kane.kanes_equations(bodies=(body1, body 2), loads=None)
    assert KM.kanes_equations(BL, loads=None)[0] == Matrix([0])
    # test for input format kane.kanes_equations(bodies=(body1, body 2))
    assert KM.kanes_equations(BL)[0] == Matrix([0])
    # test for input format kane.kanes_equations(bodies=(body1, body2), loads=[])
    assert KM.kanes_equations(BL, [])[0] == Matrix([0])
    # test for error raised when a wrong force list (in this case a string) is provided
    raises(ValueError, lambda: KM._form_fr('bad input'))

    # 1 dof problem from test_one_dof with FL & BL in instance
    KM = KanesMethod(N, [q], [u], kd, bodies=BL, forcelist=FL)
    assert KM.kanes_equations()[0] == Matrix([-c*u - k*q])

    # 2 dof problem from test_two_dof
    q1, q2, u1, u2 = dynamicsymbols('q1 q2 u1 u2')
    q1d, q2d, u1d, u2d = dynamicsymbols('q1 q2 u1 u2', 1)
    m, c1, c2, k1, k2 = symbols('m c1 c2 k1 k2')
    N = ReferenceFrame('N')
    P1 = Point('P1')
    P2 = Point('P2')
    P1.set_vel(N, u1 * N.x)
    P2.set_vel(N, (u1 + u2) * N.x)
    kd = [q1d - u1, q2d - u2]

    FL = ((P1, (-k1 * q1 - c1 * u1 + k2 * q2 + c2 * u2) * N.x), (P2, (-k2 *
        q2 - c2 * u2) * N.x))
    pa1 = Particle('pa1', P1, m)
    pa2 = Particle('pa2', P2, m)
    BL = (pa1, pa2)

    KM = KanesMethod(N, q_ind=[q1, q2], u_ind=[u1, u2], kd_eqs=kd)
    # test for input format
    # kane.kanes_equations((body1, body2), (load1, load2))
    KM.kanes_equations(BL, FL)
    MM = KM.mass_matrix
    forcing = KM.forcing
    rhs = MM.inv() * forcing
    assert expand(rhs[0]) == expand((-k1 * q1 - c1 * u1 + k2 * q2 + c2 * u2)/m)
    assert expand(rhs[1]) == expand((k1 * q1 + c1 * u1 - 2 * k2 * q2 - 2 *
                                    c2 * u2) / m)

