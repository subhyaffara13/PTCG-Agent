
def test_chaos_pendulum():
    #https://www.pydy.org/examples/chaos_pendulum.html
    mA, mB, lA, lB, IAxx, IBxx, IByy, IBzz, g = symbols('mA, mB, lA, lB, IAxx, IBxx, IByy, IBzz, g')
    theta, phi, omega, alpha = dynamicsymbols('theta phi omega alpha')

    A = ReferenceFrame('A')
    B = ReferenceFrame('B')

    with warns_deprecated_sympy():
        rod = Body('rod', mass=mA, frame=A,
                   central_inertia=inertia(A, IAxx, IAxx, 0))
        plate = Body('plate', mass=mB, frame=B,
                     central_inertia=inertia(B, IBxx, IByy, IBzz))
        C = Body('C')
    J1 = PinJoint('J1', C, rod, coordinates=theta, speeds=omega,
                  child_point=-lA * rod.z, joint_axis=C.y)
    J2 = PinJoint('J2', rod, plate, coordinates=phi, speeds=alpha,
                  parent_point=(lB - lA) * rod.z, joint_axis=rod.z)

    rod.apply_force(mA*g*C.z)
    plate.apply_force(mB*g*C.z)

    with warns_deprecated_sympy():
        method = JointsMethod(C, J1, J2)
    method.form_eoms()

    MM = method.mass_matrix
    forcing = method.forcing
    rhs = MM.LUsolve(forcing)
    xd = (-2 * IBxx * alpha * omega * sin(phi) * cos(phi) + 2 * IByy * alpha * omega * sin(phi) *
            cos(phi) - g * lA * mA * sin(theta) - g * lB * mB * sin(theta)) / (IAxx + IBxx *
                sin(phi)**2 + IByy * cos(phi)**2 + lA**2 * mA + lB**2 * mB)
    assert (rhs[0] - xd).simplify() == 0
    xd = (IBxx - IByy) * omega**2 * sin(phi) * cos(phi) / IBzz
    assert (rhs[1] - xd).simplify() == 0

