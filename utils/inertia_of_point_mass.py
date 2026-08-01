
def inertia_of_point_mass(mass, pos_vec, frame):
    sympy_deprecation_warning(
        """
        The inertia_of_point_mass function has been moved.
        Import it from "sympy.physics.mechanics".
        """,
        deprecated_since_version="1.13",
        active_deprecations_target="moved-mechanics-functions"
    )
    return _inertia_of_point_mass(mass, pos_vec, frame)


def inertia_of_point_mass(mass, pos_vec, frame):
    """Inertia dyadic of a point mass relative to point O.

    Parameters
    ==========

    mass : Sympifyable
        Mass of the point mass
    pos_vec : Vector
        Position from point O to point mass
    frame : ReferenceFrame
        Reference frame to express the dyadic in

    Examples
    ========

    >>> from sympy import symbols
    >>> from sympy.physics.mechanics import ReferenceFrame, inertia_of_point_mass
    >>> N = ReferenceFrame('N')
    >>> r, m = symbols('r m')
    >>> px = r * N.x
    >>> inertia_of_point_mass(m, px, N)
    m*r**2*(N.y|N.y) + m*r**2*(N.z|N.z)

    """

    return mass*(
        (outer(frame.x, frame.x) +
         outer(frame.y, frame.y) +
         outer(frame.z, frame.z)) *
        (pos_vec.dot(pos_vec)) - outer(pos_vec, pos_vec))

