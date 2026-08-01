
def test_invalid_coordinates():
    # Simple pendulum, but use symbols instead of dynamicsymbols
    l, m, g = symbols('l m g')
    q, u = symbols('q u')  # Generalized coordinate
    kd = [q.diff(dynamicsymbols._t) - u]
    N, O = ReferenceFrame('N'), Point('O')
    O.set_vel(N, 0)
    P = Particle('P', Point('P'), m)
    P.point.set_pos(O, l * (sin(q) * N.x - cos(q) * N.y))
    F = (P.point, -m * g * N.y)
    raises(ValueError, lambda: KanesMethod(N, [q], [u], kd, bodies=[P],
                                           forcelist=[F]))


def test_invalid_coordinates():
    # Simple pendulum, but use symbol instead of dynamicsymbol
    l, m, g = symbols('l m g')
    q = symbols('q')  # Generalized coordinate
    N, O = ReferenceFrame('N'), Point('O')
    O.set_vel(N, 0)
    P = Particle('P', Point('P'), m)
    P.point.set_pos(O, l * (sin(q) * N.x - cos(q) * N.y))
    P.potential_energy = m * g * P.point.pos_from(O).dot(N.y)
    L = Lagrangian(N, P)
    raises(ValueError, lambda: LagrangesMethod(L, [q], bodies=P))

