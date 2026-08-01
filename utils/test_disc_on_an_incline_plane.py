
def test_disc_on_an_incline_plane():
    # Disc rolling on an inclined plane
    # First the generalized coordinates are created. The mass center of the
    # disc is located from top vertex of the inclined plane by the generalized
    # coordinate 'y'. The orientation of the disc is defined by the angle
    # 'theta'. The mass of the disc is 'm' and its radius is 'R'. The length of
    # the inclined path is 'l', the angle of inclination is 'alpha'. 'g' is the
    # gravitational constant.
    y, theta = dynamicsymbols('y theta')
    yd, thetad = dynamicsymbols('y theta', 1)
    m, g, R, l, alpha = symbols('m g R l alpha')

    # Next, we create the inertial reference frame 'N'. A reference frame 'A'
    # is attached to the inclined plane. Finally a frame is created which is attached to the disk.
    N = ReferenceFrame('N')
    A = N.orientnew('A', 'Axis', [pi/2 - alpha, N.z])
    B = A.orientnew('B', 'Axis', [-theta, A.z])

    # Creating the disc 'D'; we create the point that represents the mass
    # center of the disc and set its velocity. The inertia dyadic of the disc
    # is created. Finally, we create the disc.
    Do = Point('Do')
    Do.set_vel(N, yd * A.x)
    I = m * R**2/2 * B.z | B.z
    D = RigidBody('D', Do, B, m, (I, Do))

    # To construct the Lagrangian, 'L', of the disc, we determine its kinetic
    # and potential energies, T and U, respectively. L is defined as the
    # difference between T and U.
    D.potential_energy = m * g * (l - y) * sin(alpha)
    L = Lagrangian(N, D)

    # We then create the list of generalized coordinates and constraint
    # equations. The constraint arises due to the disc rolling without slip on
    # on the inclined path. We then invoke the 'LagrangesMethod' class and
    # supply it the necessary arguments and generate the equations of motion.
    # The'rhs' method solves for the q_double_dots (i.e. the second derivative
    # with respect to time  of the generalized coordinates and the lagrange
    # multipliers.
    q = [y, theta]
    hol_coneqs = [y - R * theta]
    m = LagrangesMethod(L, q, hol_coneqs=hol_coneqs)
    m.form_lagranges_equations()
    rhs = m.rhs()
    rhs.simplify()
    assert rhs[2] == 2*g*sin(alpha)/3

