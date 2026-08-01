
def inertia(frame, ixx, iyy, izz, ixy=0, iyz=0, izx=0):
    sympy_deprecation_warning(
        """
        The inertia function has been moved.
        Import it from "sympy.physics.mechanics".
        """,
        deprecated_since_version="1.13",
        active_deprecations_target="moved-mechanics-functions"
    )
    return _inertia(frame, ixx, iyy, izz, ixy, iyz, izx)


def inertia(frame, ixx, iyy, izz, ixy=0, iyz=0, izx=0):
    """Simple way to create inertia Dyadic object.

    Explanation
    ===========

    Creates an inertia Dyadic based on the given tensor values and a body-fixed
    reference frame.

    Parameters
    ==========

    frame : ReferenceFrame
        The frame the inertia is defined in.
    ixx : Sympifyable
        The xx element in the inertia dyadic.
    iyy : Sympifyable
        The yy element in the inertia dyadic.
    izz : Sympifyable
        The zz element in the inertia dyadic.
    ixy : Sympifyable
        The xy element in the inertia dyadic.
    iyz : Sympifyable
        The yz element in the inertia dyadic.
    izx : Sympifyable
        The zx element in the inertia dyadic.

    Examples
    ========

    >>> from sympy.physics.mechanics import ReferenceFrame, inertia
    >>> N = ReferenceFrame('N')
    >>> inertia(N, 1, 2, 3)
    (N.x|N.x) + 2*(N.y|N.y) + 3*(N.z|N.z)

    """

    if not isinstance(frame, ReferenceFrame):
        raise TypeError('Need to define the inertia in a frame')
    ixx, iyy, izz = sympify(ixx), sympify(iyy), sympify(izz)
    ixy, iyz, izx = sympify(ixy), sympify(iyz), sympify(izx)
    return (ixx*outer(frame.x, frame.x) + ixy*outer(frame.x, frame.y) +
            izx*outer(frame.x, frame.z) + ixy*outer(frame.y, frame.x) +
            iyy*outer(frame.y, frame.y) + iyz*outer(frame.y, frame.z) +
            izx*outer(frame.z, frame.x) + iyz*outer(frame.z, frame.y) +
            izz*outer(frame.z, frame.z))

