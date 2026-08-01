
def test_parallel_axis():
    N = ReferenceFrame('N')
    m, Ix, Iy, Iz, a, b = symbols('m, I_x, I_y, I_z, a, b')
    Io = inertia(N, Ix, Iy, Iz)
    # Test RigidBody
    o = Point('o')
    p = o.locatenew('p', a * N.x + b * N.y)
    with warns_deprecated_sympy():
        R = Body('R', masscenter=o, frame=N, mass=m, central_inertia=Io)
    Ip = R.parallel_axis(p)
    Ip_expected = inertia(N, Ix + m * b**2, Iy + m * a**2,
                          Iz + m * (a**2 + b**2), ixy=-m * a * b)
    assert Ip == Ip_expected
    # Reference frame from which the parallel axis is viewed should not matter
    A = ReferenceFrame('A')
    A.orient_axis(N, N.z, 1)
    assert simplify(
        (R.parallel_axis(p, A) - Ip_expected).to_matrix(A)) == zeros(3, 3)
    # Test Particle
    o = Point('o')
    p = o.locatenew('p', a * N.x + b * N.y)
    with warns_deprecated_sympy():
        P = Body('P', masscenter=o, mass=m, frame=N)
    Ip = P.parallel_axis(p, N)
    Ip_expected = inertia(N, m * b ** 2, m * a ** 2, m * (a ** 2 + b ** 2),
                          ixy=-m * a * b)
    assert not P.is_rigidbody
    assert Ip == Ip_expected


def test_parallel_axis():
    # This is for a 2 dof inverted pendulum on a cart.
    # This tests the parallel axis code in KanesMethod. The inertia of the
    # pendulum is defined about the hinge, not about the center of mass.

    # Defining the constants and knowns of the system
    gravity = symbols('g')
    k, ls = symbols('k ls')
    a, mA, mC = symbols('a mA mC')
    F = dynamicsymbols('F')
    Ix, Iy, Iz = symbols('Ix Iy Iz')

    # Declaring the Generalized coordinates and speeds
    q1, q2 = dynamicsymbols('q1 q2')
    q1d, q2d = dynamicsymbols('q1 q2', 1)
    u1, u2 = dynamicsymbols('u1 u2')
    u1d, u2d = dynamicsymbols('u1 u2', 1)

    # Creating reference frames
    N = ReferenceFrame('N')
    A = ReferenceFrame('A')

    A.orient(N, 'Axis', [-q2, N.z])
    A.set_ang_vel(N, -u2 * N.z)

    # Origin of Newtonian reference frame
    O = Point('O')

    # Creating and Locating the positions of the cart, C, and the
    # center of mass of the pendulum, A
    C = O.locatenew('C', q1 * N.x)
    Ao = C.locatenew('Ao', a * A.y)

    # Defining velocities of the points
    O.set_vel(N, 0)
    C.set_vel(N, u1 * N.x)
    Ao.v2pt_theory(C, N, A)
    Cart = Particle('Cart', C, mC)
    Pendulum = RigidBody('Pendulum', Ao, A, mA, (inertia(A, Ix, Iy, Iz), C))

    # kinematical differential equations

    kindiffs = [q1d - u1, q2d - u2]

    bodyList = [Cart, Pendulum]

    forceList = [(Ao, -N.y * gravity * mA),
                 (C, -N.y * gravity * mC),
                 (C, -N.x * k * (q1 - ls)),
                 (C, N.x * F)]

    km = KanesMethod(N, [q1, q2], [u1, u2], kindiffs)
    (fr, frstar) = km.kanes_equations(bodyList, forceList)
    mm = km.mass_matrix_full
    assert mm[3, 3] == Iz


def test_parallel_axis():
    N = ReferenceFrame('N')
    m, a, b = symbols('m, a, b')
    o = Point('o')
    p = o.locatenew('p', a * N.x + b * N.y)
    P = Particle('P', o, m)
    Ip = P.parallel_axis(p, N)
    Ip_expected = inertia(N, m * b ** 2, m * a ** 2, m * (a ** 2 + b ** 2),
                          ixy=-m * a * b)
    assert Ip == Ip_expected


def test_parallel_axis():
    N = ReferenceFrame('N')
    m, Ix, Iy, Iz, a, b = symbols('m, I_x, I_y, I_z, a, b')
    Io = inertia(N, Ix, Iy, Iz)
    o = Point('o')
    p = o.locatenew('p', a * N.x + b * N.y)
    R = RigidBody('R', o, N, m, (Io, o))
    Ip = R.parallel_axis(p)
    Ip_expected = inertia(N, Ix + m * b**2, Iy + m * a**2,
                          Iz + m * (a**2 + b**2), ixy=-m * a * b)
    assert Ip == Ip_expected
    # Reference frame from which the parallel axis is viewed should not matter
    A = ReferenceFrame('A')
    A.orient_axis(N, N.z, 1)
    assert simplify(
        (R.parallel_axis(p, A) - Ip_expected).to_matrix(A)) == zeros(3, 3)

