
def _create_rolling_disc():
    # Define symbols and coordinates
    t = dynamicsymbols._t
    q1, q2, q3, q4, q5, u1, u2, u3, u4, u5 = dynamicsymbols('q1:6 u1:6')
    g, r, m = symbols('g r m')
    # Define bodies and frames
    ground = RigidBody('ground')
    disc = RigidBody('disk', mass=m)
    disc.inertia = (m * r ** 2 / 4 * inertia(disc.frame, 1, 2, 1),
                    disc.masscenter)
    ground.masscenter.set_vel(ground.frame, 0)
    disc.masscenter.set_vel(disc.frame, 0)
    int_frame = ReferenceFrame('int_frame')
    # Orient frames
    int_frame.orient_body_fixed(ground.frame, (q1, q2, 0), 'zxy')
    disc.frame.orient_axis(int_frame, int_frame.y, q3)
    g_w_d = disc.frame.ang_vel_in(ground.frame)
    disc.frame.set_ang_vel(ground.frame,
                           u1 * disc.x + u2 * disc.y + u3 * disc.z)
    # Define points
    cp = ground.masscenter.locatenew('contact_point',
                                     q4 * ground.x + q5 * ground.y)
    cp.set_vel(ground.frame, u4 * ground.x + u5 * ground.y)
    disc.masscenter.set_pos(cp, r * int_frame.z)
    disc.masscenter.set_vel(ground.frame, cross(
        disc.frame.ang_vel_in(ground.frame), disc.masscenter.pos_from(cp)))
    # Define kinematic differential equations
    kdes = [g_w_d.dot(disc.x) - u1, g_w_d.dot(disc.y) - u2,
            g_w_d.dot(disc.z) - u3, q4.diff(t) - u4, q5.diff(t) - u5]
    # Define nonholonomic constraints
    v0 = cp.vel(ground.frame) + cross(
        disc.frame.ang_vel_in(int_frame), cp.pos_from(disc.masscenter))
    fnh = [v0.dot(ground.x), v0.dot(ground.y)]
    # Define loads
    loads = [(disc.masscenter, -disc.mass * g * ground.z)]
    bodies = [disc]
    return {
        'frame': ground.frame,
        'q_ind': [q1, q2, q3, q4, q5],
        'u_ind': [u1, u2, u3],
        'u_dep': [u4, u5],
        'kdes': kdes,
        'fnh': fnh,
        'bodies': bodies,
        'loads': loads
    }

