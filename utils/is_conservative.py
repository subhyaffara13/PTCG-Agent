
def is_conservative(field):
    """
    Checks if a field is conservative.

    Parameters
    ==========

    field : Vector
        The field to check for conservative property

    Examples
    ========

    >>> from sympy.vector import CoordSys3D
    >>> from sympy.vector import is_conservative
    >>> R = CoordSys3D('R')
    >>> is_conservative(R.y*R.z*R.i + R.x*R.z*R.j + R.x*R.y*R.k)
    True
    >>> is_conservative(R.z*R.j)
    False

    """

    # Field is conservative irrespective of system
    # Take the first coordinate system in the result of the
    # separate method of Vector
    if not isinstance(field, Vector):
        raise TypeError("field should be a Vector")
    if field == Vector.zero:
        return True
    return curl(field).simplify() == Vector.zero


def is_conservative(field):
    """
    Checks if a field is conservative.

    Parameters
    ==========

    field : Vector
        The field to check for conservative property

    Examples
    ========

    >>> from sympy.physics.vector import ReferenceFrame
    >>> from sympy.physics.vector import is_conservative
    >>> R = ReferenceFrame('R')
    >>> is_conservative(R[1]*R[2]*R.x + R[0]*R[2]*R.y + R[0]*R[1]*R.z)
    True
    >>> is_conservative(R[2] * R.y)
    False

    """

    # Field is conservative irrespective of frame
    # Take the first frame in the result of the separate method of Vector
    if field == Vector(0):
        return True
    frame = list(field.separate())[0]
    return curl(field, frame).simplify() == Vector(0)

