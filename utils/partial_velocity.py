
def partial_velocity(vel_vecs, gen_speeds, frame):
    """Returns a list of partial velocities with respect to the provided
    generalized speeds in the given reference frame for each of the supplied
    velocity vectors.

    The output is a list of lists. The outer list has a number of elements
    equal to the number of supplied velocity vectors. The inner lists are, for
    each velocity vector, the partial derivatives of that velocity vector with
    respect to the generalized speeds supplied.

    Parameters
    ==========

    vel_vecs : iterable
        An iterable of velocity vectors (angular or linear).
    gen_speeds : iterable
        An iterable of generalized speeds.
    frame : ReferenceFrame
        The reference frame that the partial derivatives are going to be taken
        in.

    Examples
    ========

    >>> from sympy.physics.vector import Point, ReferenceFrame
    >>> from sympy.physics.vector import dynamicsymbols
    >>> from sympy.physics.vector import partial_velocity
    >>> u = dynamicsymbols('u')
    >>> N = ReferenceFrame('N')
    >>> P = Point('P')
    >>> P.set_vel(N, u * N.x)
    >>> vel_vecs = [P.vel(N)]
    >>> gen_speeds = [u]
    >>> partial_velocity(vel_vecs, gen_speeds, N)
    [[N.x]]

    """

    if not iterable(vel_vecs):
        raise TypeError('Velocity vectors must be contained in an iterable.')

    if not iterable(gen_speeds):
        raise TypeError('Generalized speeds must be contained in an iterable')

    vec_partials = []
    gen_speeds = list(gen_speeds)
    for vel in vel_vecs:
        partials = [Vector(0) for _ in gen_speeds]
        for components, ref in vel.args:
            mat, _ = linear_eq_to_matrix(components, gen_speeds)
            for i in range(len(gen_speeds)):
                for dim, direction in enumerate(ref):
                    if mat[dim, i] != 0:
                        partials[i] += direction * mat[dim, i]

        vec_partials.append(partials)

    return vec_partials

