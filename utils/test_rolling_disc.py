
def test_rolling_disc():
    # Rolling Disc Example
    # Here the rolling disc is formed from the contact point up, removing the
    # need to introduce generalized speeds. Only 3 configuration and three
    # speed variables are need to describe this system, along with the disc's
    # mass and radius, and the local gravity (note that mass will drop out).
    q1, q2, q3, u1, u2, u3 = dynamicsymbols('q1 q2 q3 u1 u2 u3')
    q1d, q2d, q3d, u1d, u2d, u3d = dynamicsymbols('q1 q2 q3 u1 u2 u3', 1)
    r, m, g = symbols('r m g')

    # The kinematics are formed by a series of simple rotations. Each simple
    # rotation creates a new frame, and the next rotation is defined by the new
    # frame's basis vectors. This example uses a 3-1-2 series of rotations, or
    # Z, X, Y series of rotations. Angular velocity for this is defined using
    # the second frame's basis (the lean frame).
    N = ReferenceFrame('N')
    Y = N.orientnew('Y', 'Axis', [q1, N.z])
    L = Y.orientnew('L', 'Axis', [q2, Y.x])
    R = L.orientnew('R', 'Axis', [q3, L.y])
    w_R_N_qd = R.ang_vel_in(N)
    R.set_ang_vel(N, u1 * L.x + u2 * L.y + u3 * L.z)

    # This is the translational kinematics. We create a point with no velocity
    # in N; this is the contact point between the disc and ground. Next we form
    # the position vector from the contact point to the disc's center of mass.
    # Finally we form the velocity and acceleration of the disc.
    C = Point('C')
    C.set_vel(N, 0)
    Dmc = C.locatenew('Dmc', r * L.z)
    Dmc.v2pt_theory(C, N, R)

    # This is a simple way to form the inertia dyadic.
    I = inertia(L, m / 4 * r**2, m / 2 * r**2, m / 4 * r**2)

    # Kinematic differential equations; how the generalized coordinate time
    # derivatives relate to generalized speeds.
    kd = [dot(R.ang_vel_in(N) - w_R_N_qd, uv) for uv in L]

    # Creation of the force list; it is the gravitational force at the mass
    # center of the disc. Then we create the disc by assigning a Point to the
    # center of mass attribute, a ReferenceFrame to the frame attribute, and mass
    # and inertia. Then we form the body list.
    ForceList = [(Dmc, - m * g * Y.z)]
    BodyD = RigidBody('BodyD', Dmc, R, m, (I, Dmc))
    BodyList = [BodyD]

    # Finally we form the equations of motion, using the same steps we did
    # before. Specify inertial frame, supply generalized speeds, supply
    # kinematic differential equation dictionary, compute Fr from the force
    # list and Fr* from the body list, compute the mass matrix and forcing
    # terms, then solve for the u dots (time derivatives of the generalized
    # speeds).
    KM = KanesMethod(N, q_ind=[q1, q2, q3], u_ind=[u1, u2, u3], kd_eqs=kd)
    KM.kanes_equations(BodyList, ForceList)
    MM = KM.mass_matrix
    forcing = KM.forcing
    rhs = MM.inv() * forcing
    kdd = KM.kindiffdict()
    rhs = rhs.subs(kdd)
    rhs.simplify()
    assert rhs.expand() == Matrix([(6*u2*u3*r - u3**2*r*tan(q2) +
        4*g*sin(q2))/(5*r), -2*u1*u3/3, u1*(-2*u2 + u3*tan(q2))]).expand()
    assert simplify(KM.rhs() -
                    KM.mass_matrix_full.LUsolve(KM.forcing_full)) == zeros(6, 1)

    # This code tests our output vs. benchmark values. When r=g=m=1, the
    # critical speed (where all eigenvalues of the linearized equations are 0)
    # is 1 / sqrt(3) for the upright case.
    A = KM.linearize(A_and_B=True)[0]
    A_upright = A.subs({r: 1, g: 1, m: 1}).subs({q1: 0, q2: 0, q3: 0, u1: 0, u3: 0})
    import sympy
    assert sympy.sympify(A_upright.subs({u2: 1 / sqrt(3)})).eigenvals() == {S.Zero: 6}


def test_rolling_disc():
    # Rolling Disc Example
    # Here the rolling disc is formed from the contact point up, removing the
    # need to introduce generalized speeds. Only 3 configuration and 3
    # speed variables are need to describe this system, along with the
    # disc's mass and radius, and the local gravity.
    q1, q2, q3 = dynamicsymbols('q1 q2 q3')
    q1d, q2d, q3d = dynamicsymbols('q1 q2 q3', 1)
    r, m, g = symbols('r m g')

    # The kinematics are formed by a series of simple rotations. Each simple
    # rotation creates a new frame, and the next rotation is defined by the new
    # frame's basis vectors. This example uses a 3-1-2 series of rotations, or
    # Z, X, Y series of rotations. Angular velocity for this is defined using
    # the second frame's basis (the lean frame).
    N = ReferenceFrame('N')
    Y = N.orientnew('Y', 'Axis', [q1, N.z])
    L = Y.orientnew('L', 'Axis', [q2, Y.x])
    R = L.orientnew('R', 'Axis', [q3, L.y])

    # This is the translational kinematics. We create a point with no velocity
    # in N; this is the contact point between the disc and ground. Next we form
    # the position vector from the contact point to the disc's center of mass.
    # Finally we form the velocity and acceleration of the disc.
    C = Point('C')
    C.set_vel(N, 0)
    Dmc = C.locatenew('Dmc', r * L.z)
    Dmc.v2pt_theory(C, N, R)

    # Forming the inertia dyadic.
    I = inertia(L, m/4 * r**2, m/2 * r**2, m/4 * r**2)
    BodyD = RigidBody('BodyD', Dmc, R, m, (I, Dmc))

    # Finally we form the equations of motion, using the same steps we did
    # before. Supply the Lagrangian, the generalized speeds.
    BodyD.potential_energy = - m * g * r * cos(q2)
    Lag = Lagrangian(N, BodyD)
    q = [q1, q2, q3]
    q1 = Function('q1')
    q2 = Function('q2')
    q3 = Function('q3')
    l = LagrangesMethod(Lag, q)
    l.form_lagranges_equations()
    RHS = l.rhs()
    RHS.simplify()
    t = symbols('t')

    assert (l.mass_matrix[3:6] == [0, 5*m*r**2/4, 0])
    assert RHS[4].simplify() == (
        (-8*g*sin(q2(t)) + r*(5*sin(2*q2(t))*Derivative(q1(t), t) +
        12*cos(q2(t))*Derivative(q3(t), t))*Derivative(q1(t), t))/(10*r))
    assert RHS[5] == (-5*cos(q2(t))*Derivative(q1(t), t) + 6*tan(q2(t)
        )*Derivative(q3(t), t) + 4*Derivative(q1(t), t)/cos(q2(t))
        )*Derivative(q2(t), t)

