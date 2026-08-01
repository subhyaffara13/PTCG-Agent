
def test_deprecated_set_potential_energy():
    m, g, h = symbols('m g h')
    P = Point('P')
    p = Particle('pa', P, m)
    with warns_deprecated_sympy():
        p.set_potential_energy(m * g * h)


def test_deprecated_set_potential_energy():
    m, g, h = symbols('m g h')
    A = ReferenceFrame('A')
    P = Point('P')
    I = Dyadic(0)
    B = RigidBody('B', P, A, m, (I, P))
    with warns_deprecated_sympy():
        B.set_potential_energy(m*g*h)

