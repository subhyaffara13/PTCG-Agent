
def test_implicit_kinematics():
    # Test that implicit kinematics can handle complicated
    # equations that explicit form struggles with
    # See https://github.com/sympy/sympy/issues/22626

    # Inertial frame
    NED = ReferenceFrame('NED')
    NED_o = Point('NED_o')
    NED_o.set_vel(NED, 0)

    # body frame
    q_att = dynamicsymbols('lambda_0:4', real=True)
    B = NED.orientnew('B', 'Quaternion', q_att)

    # Generalized coordinates
    q_pos = dynamicsymbols('B_x:z')
    B_cm = NED_o.locatenew('B_cm', q_pos[0]*B.x + q_pos[1]*B.y + q_pos[2]*B.z)

    q_ind = q_att[1:] + q_pos
    q_dep = [q_att[0]]

    kinematic_eqs = []

    # Generalized velocities
    B_ang_vel = B.ang_vel_in(NED)
    P, Q, R = dynamicsymbols('P Q R')
    B.set_ang_vel(NED, P*B.x + Q*B.y + R*B.z)

    B_ang_vel_kd = (B.ang_vel_in(NED) - B_ang_vel).simplify()

    # Equating the two gives us the kinematic equation
    kinematic_eqs += [
        B_ang_vel_kd & B.x,
        B_ang_vel_kd & B.y,
        B_ang_vel_kd & B.z
    ]

    B_cm_vel = B_cm.vel(NED)
    U, V, W = dynamicsymbols('U V W')
    B_cm.set_vel(NED, U*B.x + V*B.y + W*B.z)

    # Compute the velocity of the point using the two methods
    B_ref_vel_kd = (B_cm.vel(NED) - B_cm_vel)

    # taking dot product with unit vectors to get kinematic equations
    # relating body coordinates and velocities

    # Note, there is a choice to dot with NED.xyz here. That makes
    # the implicit form have some bigger terms but is still fine, the
    # explicit form still struggles though
    kinematic_eqs += [
                      B_ref_vel_kd & B.x,
                      B_ref_vel_kd & B.y,
                      B_ref_vel_kd & B.z,
                     ]

    u_ind = [U, V, W, P, Q, R]

    # constraints
    q_att_vec = Matrix(q_att)
    config_cons = [(q_att_vec.T*q_att_vec)[0] - 1] #unit norm
    kinematic_eqs = kinematic_eqs + [(q_att_vec.T * q_att_vec.diff())[0]]

    try:
        KM = KanesMethod(NED, q_ind, u_ind,
          q_dependent= q_dep,
          kd_eqs = kinematic_eqs,
          configuration_constraints = config_cons,
          velocity_constraints= [],
          u_dependent= [], #no dependent speeds
          u_auxiliary = [], # No auxiliary speeds
          explicit_kinematics = False # implicit kinematics
        )
    except Exception as e:
        raise e

    # mass and inertia dyadic relative to CM
    M_B = symbols('M_B')
    J_B = inertia(B, *[S(f'J_B_{ax}')*(1 if ax[0] == ax[1] else -1)
            for ax in ['xx', 'yy', 'zz', 'xy', 'yz', 'xz']])
    J_B = J_B.subs({S('J_B_xy'): 0, S('J_B_yz'): 0})
    RB = RigidBody('RB', B_cm, B, M_B, (J_B, B_cm))

    rigid_bodies = [RB]
    # Forces
    force_list = [
        #gravity pointing down
        (RB.masscenter, RB.mass*S('g')*NED.z),
        #generic forces and torques in body frame(inputs)
        (RB.frame, dynamicsymbols('T_z')*B.z),
        (RB.masscenter, dynamicsymbols('F_z')*B.z)
    ]

    KM.kanes_equations(rigid_bodies, force_list)

    # Expecting implicit form to be less than 5% of the flops
    n_ops_implicit = sum(
        [x.count_ops() for x in KM.forcing_full] +
        [x.count_ops() for x in KM.mass_matrix_full]
    )
    # Save implicit kinematic matrices to use later
    mass_matrix_kin_implicit = KM.mass_matrix_kin
    forcing_kin_implicit = KM.forcing_kin

    KM.explicit_kinematics = True
    n_ops_explicit = sum(
        [x.count_ops() for x in KM.forcing_full] +
        [x.count_ops() for x in KM.mass_matrix_full]
    )
    forcing_kin_explicit = KM.forcing_kin

    assert n_ops_implicit / n_ops_explicit < .05

    # Ideally we would check that implicit and explicit equations give the same result as done in test_one_dof
    # But the whole raison-d'etre of the implicit equations is to deal with problems such
    # as this one where the explicit form is too complicated to handle, especially the angular part
    # (i.e. tests would be too slow)
    # Instead, we check that the kinematic equations are correct using more fundamental tests:
    #
    # (1) that we recover the kinematic equations we have provided
    assert (mass_matrix_kin_implicit * KM.q.diff() - forcing_kin_implicit) == Matrix(kinematic_eqs)

    # (2) that rate of quaternions matches what 'textbook' solutions give
    # Note that we just use the explicit kinematics for the linear velocities
    # as they are not as complicated as the angular ones
    qdot_candidate = forcing_kin_explicit

    quat_dot_textbook = Matrix([
        [0, -P, -Q, -R],
        [P,  0,  R, -Q],
        [Q, -R,  0,  P],
        [R,  Q, -P,  0],
    ]) * q_att_vec / 2

    # Again, if we don't use this "textbook" solution
    # sympy will struggle to deal with the terms related to quaternion rates
    # due to the number of operations involved
    qdot_candidate[-1] = quat_dot_textbook[0] # lambda_0, note the [-1] as sympy's Kane puts the dependent coordinate last
    qdot_candidate[0]  = quat_dot_textbook[1] # lambda_1
    qdot_candidate[1]  = quat_dot_textbook[2] # lambda_2
    qdot_candidate[2]  = quat_dot_textbook[3] # lambda_3

    # sub the config constraint in the candidate solution and compare to the implicit rhs
    lambda_0_sol = solve(config_cons[0], q_att_vec[0])[1]
    lhs_candidate = simplify(mass_matrix_kin_implicit * qdot_candidate).subs({q_att_vec[0]: lambda_0_sol})
    assert lhs_candidate == forcing_kin_implicit

