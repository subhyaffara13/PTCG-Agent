
def test_kinetic_energy():
    m, M, l1 = symbols('m M l1')
    omega = dynamicsymbols('omega')
    N = ReferenceFrame('N')
    O = Point('O')
    O.set_vel(N, 0 * N.x)
    Ac = O.locatenew('Ac', l1 * N.x)
    P = Ac.locatenew('P', l1 * N.x)
    a = ReferenceFrame('a')
    a.set_ang_vel(N, omega * N.z)
    Ac.v2pt_theory(O, N, a)
    P.v2pt_theory(O, N, a)
    Pa = Particle('Pa', P, m)
    I = outer(N.z, N.z)
    A = RigidBody('A', Ac, a, M, (I, Ac))
    raises(TypeError, lambda: kinetic_energy(Pa, Pa, A))
    raises(TypeError, lambda: kinetic_energy(N, N, A))
    assert 0 == (kinetic_energy(N, Pa, A) - (M*l1**2*omega**2/2
            + 2*l1**2*m*omega**2 + omega**2/2)).expand()

