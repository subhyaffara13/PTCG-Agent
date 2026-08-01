
def rot_ccw_axis2(theta):
    r"""Returns a rotation matrix for a rotation of theta (in radians)
    about the 2-axis.

    Explanation
    ===========

    For a right-handed coordinate system, this corresponds to a
    counterclockwise rotation around the `y`-axis, given by:

    .. math::

        R  = \begin{bmatrix}
                 \cos(\theta) & 0 & \sin(\theta) \\
                            0 & 1 &            0 \\
                -\sin(\theta) & 0 & \cos(\theta)
            \end{bmatrix}

    Examples
    ========

    >>> from sympy import pi, rot_ccw_axis2

    A rotation of pi/3 (60 degrees):

    >>> theta = pi/3
    >>> rot_ccw_axis2(theta)
    Matrix([
    [       1/2, 0, sqrt(3)/2],
    [         0, 1,         0],
    [-sqrt(3)/2, 0,       1/2]])

    If we rotate by pi/2 (90 degrees):

    >>> rot_ccw_axis2(pi/2)
    Matrix([
    [ 0,  0,  1],
    [ 0,  1,  0],
    [-1,  0,  0]])

    See Also
    ========

    rot_givens: Returns a Givens rotation matrix (generalized rotation for
        any number of dimensions)
    rot_axis2: Returns a rotation matrix for a rotation of theta (in radians)
        about the 2-axis (clockwise around the y axis)
    rot_ccw_axis1: Returns a rotation matrix for a rotation of theta (in radians)
        about the 1-axis (counterclockwise around the x axis)
    rot_ccw_axis3: Returns a rotation matrix for a rotation of theta (in radians)
        about the 3-axis (counterclockwise around the z axis)
    """
    return rot_givens(0, 2, theta, dim=3)

