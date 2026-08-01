
def test_pin_joint_double_pendulum():
    q1, q2 = dynamicsymbols('q1 q2')
    u1, u2 = dynamicsymbols('u1 u2')
    m, l = symbols('m l')
    N = ReferenceFrame('N')
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    C = RigidBody('C', frame=N)  # ceiling
    PartP = RigidBody('P', frame=A, mass=m)
    PartR = RigidBody('R', frame=B, mass=m)

    J1 = PinJoint('J1', C, PartP, speeds=u1, coordinates=q1,
                  child_point=-l*A.x, joint_axis=C.frame.z)
    J2 = PinJoint('J2', PartP, PartR, speeds=u2, coordinates=q2,
                  child_point=-l*B.x, joint_axis=PartP.frame.z)

    # Check orientation
    assert N.dcm(A) == Matrix([[cos(q1), -sin(q1), 0],
                               [sin(q1), cos(q1), 0], [0, 0, 1]])
    assert A.dcm(B) == Matrix([[cos(q2), -sin(q2), 0],
                               [sin(q2), cos(q2), 0], [0, 0, 1]])
    assert simplify(N.dcm(B)) == Matrix([[cos(q1 + q2), -sin(q1 + q2), 0],
                                                 [sin(q1 + q2), cos(q1 + q2), 0],
                                                 [0, 0, 1]])

    # Check Angular Velocity
    assert A.ang_vel_in(N) == u1 * N.z
    assert B.ang_vel_in(A) == u2 * A.z
    assert B.ang_vel_in(N) == u1 * N.z + u2 * A.z

    # Check kde
    assert J1.kdes == Matrix([u1 - q1.diff(t)])
    assert J2.kdes == Matrix([u2 - q2.diff(t)])

    # Check Linear Velocity
    assert PartP.masscenter.vel(N) == l*u1*A.y
    assert PartR.masscenter.vel(A) == l*u2*B.y
    assert PartR.masscenter.vel(N) == l*u1*A.y + l*(u1 + u2)*B.y

