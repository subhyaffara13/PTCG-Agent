
def angular_momentum(point, frame, *body):
    """Angular momentum of a system.

    Explanation
    ===========

    This function returns the angular momentum of a system of Particle's and/or
    RigidBody's. The angular momentum of such a system is equal to the vector
    sum of the angular momentum of its constituents. Consider a system, S,
    comprised of a rigid body, A, and a particle, P. The angular momentum of
    the system, H, is equal to the vector sum of the angular momentum of the
    particle, H1, and the angular momentum of the rigid body, H2, i.e.

    H = H1 + H2

    Parameters
    ==========

    point : Point
        The point about which angular momentum of the system is desired.
    frame : ReferenceFrame
        The frame in which angular momentum is desired.
    body1, body2, body3... : Particle and/or RigidBody
        The body (or bodies) whose angular momentum is required.

    Examples
    ========

    >>> from sympy.physics.mechanics import Point, Particle, ReferenceFrame
    >>> from sympy.physics.mechanics import RigidBody, outer, angular_momentum
    >>> N = ReferenceFrame('N')
    >>> O = Point('O')
    >>> O.set_vel(N, 0 * N.x)
    >>> P = O.locatenew('P', 1 * N.x)
    >>> P.set_vel(N, 10 * N.x)
    >>> Pa = Particle('Pa', P, 1)
    >>> Ac = O.locatenew('Ac', 2 * N.y)
    >>> Ac.set_vel(N, 5 * N.y)
    >>> a = ReferenceFrame('a')
    >>> a.set_ang_vel(N, 10 * N.z)
    >>> I = outer(N.z, N.z)
    >>> A = RigidBody('A', Ac, a, 20, (I, Ac))
    >>> angular_momentum(O, N, Pa, A)
    10*N.z

    """

    if not isinstance(frame, ReferenceFrame):
        raise TypeError('Please enter a valid ReferenceFrame')
    if not isinstance(point, Point):
        raise TypeError('Please specify a valid Point')
    else:
        angular_momentum_sys = Vector(0)
        for e in body:
            if isinstance(e, (RigidBody, Particle)):
                angular_momentum_sys += e.angular_momentum(point, frame)
            else:
                raise TypeError('*body must have only Particle or RigidBody')
    return angular_momentum_sys

