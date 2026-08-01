
def directional_derivative(field, direction_vector):
    """
    Returns the directional derivative of a scalar or vector field computed
    along a given vector in coordinate system which parameters are expressed.

    Parameters
    ==========

    field : Vector or Scalar
        The scalar or vector field to compute the directional derivative of

    direction_vector : Vector
        The vector to calculated directional derivative along them.


    Examples
    ========

    >>> from sympy.vector import CoordSys3D, directional_derivative
    >>> R = CoordSys3D('R')
    >>> f1 = R.x*R.y*R.z
    >>> v1 = 3*R.i + 4*R.j + R.k
    >>> directional_derivative(f1, v1)
    R.x*R.y + 4*R.x*R.z + 3*R.y*R.z
    >>> f2 = 5*R.x**2*R.z
    >>> directional_derivative(f2, v1)
    5*R.x**2 + 30*R.x*R.z

    """
    from sympy.vector.operators import _get_coord_systems
    coord_sys = _get_coord_systems(field)
    if len(coord_sys) > 0:
        # TODO: This gets a random coordinate system in case of multiple ones:
        coord_sys = next(iter(coord_sys))
        field = express(field, coord_sys, variables=True)
        i, j, k = coord_sys.base_vectors()
        x, y, z = coord_sys.base_scalars()
        out = Vector.dot(direction_vector, i) * diff(field, x)
        out += Vector.dot(direction_vector, j) * diff(field, y)
        out += Vector.dot(direction_vector, k) * diff(field, z)
        if out == 0 and isinstance(field, Vector):
            out = Vector.zero
        return out
    elif isinstance(field, Vector):
        return Vector.zero
    else:
        return S.Zero

