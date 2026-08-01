
def gravity(acceleration, *bodies):
    from sympy.physics.mechanics.loads import gravity as _gravity
    sympy_deprecation_warning(
        """
        The gravity function has been moved.
        Import it from "sympy.physics.mechanics.loads".
        """,
        deprecated_since_version="1.13",
        active_deprecations_target="moved-mechanics-functions"
    )
    return _gravity(acceleration, *bodies)


def gravity(acceleration, *bodies):
    """
    Returns a list of gravity forces given the acceleration
    due to gravity and any number of particles or rigidbodies.

    Example
    =======

    >>> from sympy.physics.mechanics import ReferenceFrame, Particle, RigidBody
    >>> from sympy.physics.mechanics.loads import gravity
    >>> from sympy import symbols
    >>> N = ReferenceFrame('N')
    >>> g = symbols('g')
    >>> P = Particle('P')
    >>> B = RigidBody('B')
    >>> gravity(g*N.y, P, B)
    [(P_masscenter, P_mass*g*N.y),
     (B_masscenter, B_mass*g*N.y)]

    """

    gravity_force = []
    for body in bodies:
        if not isinstance(body, BodyBase):
            raise TypeError(f'{type(body)} is not a body type')
        gravity_force.append(Force(body.masscenter, body.mass * acceleration))
    return gravity_force

