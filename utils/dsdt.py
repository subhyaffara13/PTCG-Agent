
def dsdt(s_augmented: chex.Array, _: float, params: EnvParams) -> chex.Array:
    """Compute time derivative of the state change - Use for ODE int."""
    m1, m2 = params.link_mass_1, params.link_mass_2
    l1 = params.link_length_1
    lc1, lc2 = params.link_com_pos_1, params.link_com_pos_2
    i1, i2 = params.link_moi, params.link_moi
    g = 9.8
    a = s_augmented[-1]
    s = s_augmented[:-1]
    theta1, theta2, dtheta1, dtheta2 = s
    d1 = m1 * lc1**2 + m2 * (l1**2 + lc2**2 + 2 * l1 * lc2 * jnp.cos(theta2)) + i1 + i2
    d2 = m2 * (lc2**2 + l1 * lc2 * jnp.cos(theta2)) + i2
    phi2 = m2 * lc2 * g * jnp.cos(theta1 + theta2 - jnp.pi / 2.0)
    phi1 = (
        -m2 * l1 * lc2 * dtheta2**2 * jnp.sin(theta2)
        - 2 * m2 * l1 * lc2 * dtheta2 * dtheta1 * jnp.sin(theta2)
        + (m1 * lc1 + m2 * l1) * g * jnp.cos(theta1 - jnp.pi / 2)
        + phi2
    )
    ddtheta2 = (
        a + d2 / d1 * phi1 - m2 * l1 * lc2 * dtheta1**2 * jnp.sin(theta2) - phi2
    ) / (m2 * lc2**2 + i2 - d2**2 / d1)
    ddtheta1 = -(d2 * ddtheta2 + phi1) / d1
    return jnp.array([dtheta1, dtheta2, ddtheta1, ddtheta2, 0.0])

