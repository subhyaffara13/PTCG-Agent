
def express(expr, system, system2=None, variables=False):
    """
    Global function for 'express' functionality.

    Re-expresses a Vector, Dyadic or scalar(sympyfiable) in the given
    coordinate system.

    If 'variables' is True, then the coordinate variables (base scalars)
    of other coordinate systems present in the vector/scalar field or
    dyadic are also substituted in terms of the base scalars of the
    given system.

    Parameters
    ==========

    expr : Vector/Dyadic/scalar(sympyfiable)
        The expression to re-express in CoordSys3D 'system'

    system: CoordSys3D
        The coordinate system the expr is to be expressed in

    system2: CoordSys3D
        The other coordinate system required for re-expression
        (only for a Dyadic Expr)

    variables : boolean
        Specifies whether to substitute the coordinate variables present
        in expr, in terms of those of parameter system

    Examples
    ========

    >>> from sympy.vector import CoordSys3D
    >>> from sympy import Symbol, cos, sin
    >>> N = CoordSys3D('N')
    >>> q = Symbol('q')
    >>> B = N.orient_new_axis('B', q, N.k)
    >>> from sympy.vector import express
    >>> express(B.i, N)
    (cos(q))*N.i + (sin(q))*N.j
    >>> express(N.x, B, variables=True)
    B.x*cos(q) - B.y*sin(q)
    >>> d = N.i.outer(N.i)
    >>> express(d, B, N) == (cos(q))*(B.i|N.i) + (-sin(q))*(B.j|N.i)
    True

    """

    if expr in (0, Vector.zero):
        return expr

    if not isinstance(system, CoordSys3D):
        raise TypeError("system should be a CoordSys3D \
                        instance")

    if isinstance(expr, Vector):
        if system2 is not None:
            raise ValueError("system2 should not be provided for \
                                Vectors")
        # Given expr is a Vector
        if variables:
            # If variables attribute is True, substitute
            # the coordinate variables in the Vector
            system_list = {x.system for x in expr.atoms(BaseScalar, BaseVector)} - {system}
            subs_dict = {}
            for f in system_list:
                subs_dict.update(f.scalar_map(system))
            expr = expr.subs(subs_dict)
        # Re-express in this coordinate system
        outvec = Vector.zero
        parts = expr.separate()
        for x in parts:
            if x != system:
                temp = system.rotation_matrix(x) * parts[x].to_matrix(x)
                outvec += matrix_to_vector(temp, system)
            else:
                outvec += parts[x]
        return outvec

    elif isinstance(expr, Dyadic):
        if system2 is None:
            system2 = system
        if not isinstance(system2, CoordSys3D):
            raise TypeError("system2 should be a CoordSys3D \
                            instance")
        outdyad = Dyadic.zero
        var = variables
        for k, v in expr.components.items():
            outdyad += (express(v, system, variables=var) *
                        (express(k.args[0], system, variables=var) |
                         express(k.args[1], system2, variables=var)))

        return outdyad

    else:
        if system2 is not None:
            raise ValueError("system2 should not be provided for \
                                Vectors")
        if variables:
            # Given expr is a scalar field
            system_set = set()
            expr = sympify(expr)
            # Substitute all the coordinate variables
            for x in expr.atoms(BaseScalar):
                if x.system != system:
                    system_set.add(x.system)
            subs_dict = {}
            for f in system_set:
                subs_dict.update(f.scalar_map(system))
            return expr.subs(subs_dict)
        return expr


def express(expr, frame, frame2=None, variables=False):
    """
    Global function for 'express' functionality.

    Re-expresses a Vector, scalar(sympyfiable) or Dyadic in given frame.

    Refer to the local methods of Vector and Dyadic for details.
    If 'variables' is True, then the coordinate variables (CoordinateSym
    instances) of other frames present in the vector/scalar field or
    dyadic expression are also substituted in terms of the base scalars of
    this frame.

    Parameters
    ==========

    expr : Vector/Dyadic/scalar(sympyfiable)
        The expression to re-express in ReferenceFrame 'frame'

    frame: ReferenceFrame
        The reference frame to express expr in

    frame2 : ReferenceFrame
        The other frame required for re-expression(only for Dyadic expr)

    variables : boolean
        Specifies whether to substitute the coordinate variables present
        in expr, in terms of those of frame

    Examples
    ========

    >>> from sympy.physics.vector import ReferenceFrame, outer, dynamicsymbols
    >>> from sympy.physics.vector import init_vprinting
    >>> init_vprinting(pretty_print=False)
    >>> N = ReferenceFrame('N')
    >>> q = dynamicsymbols('q')
    >>> B = N.orientnew('B', 'Axis', [q, N.z])
    >>> d = outer(N.x, N.x)
    >>> from sympy.physics.vector import express
    >>> express(d, B, N)
    cos(q)*(B.x|N.x) - sin(q)*(B.y|N.x)
    >>> express(B.x, N)
    cos(q)*N.x + sin(q)*N.y
    >>> express(N[0], B, variables=True)
    B_x*cos(q) - B_y*sin(q)

    """

    _check_frame(frame)

    if expr == 0:
        return expr

    if isinstance(expr, Vector):
        # Given expr is a Vector
        if variables:
            # If variables attribute is True, substitute the coordinate
            # variables in the Vector
            frame_list = [x[-1] for x in expr.args]
            subs_dict = {}
            for f in frame_list:
                subs_dict.update(f.variable_map(frame))
            expr = expr.subs(subs_dict)
        # Re-express in this frame
        outvec = Vector([])
        for v in expr.args:
            if v[1] != frame:
                temp = frame.dcm(v[1]) * v[0]
                if Vector.simp:
                    temp = temp.applyfunc(lambda x:
                                          trigsimp(x, method='fu'))
                outvec += Vector([(temp, frame)])
            else:
                outvec += Vector([v])
        return outvec

    if isinstance(expr, Dyadic):
        if frame2 is None:
            frame2 = frame
        _check_frame(frame2)
        ol = Dyadic(0)
        for v in expr.args:
            ol += express(v[0], frame, variables=variables) * \
                  (express(v[1], frame, variables=variables) |
                   express(v[2], frame2, variables=variables))
        return ol

    else:
        if variables:
            # Given expr is a scalar field
            frame_set = set()
            expr = sympify(expr)
            # Substitute all the coordinate variables
            for x in expr.free_symbols:
                if isinstance(x, CoordinateSym) and x.frame != frame:
                    frame_set.add(x.frame)
            subs_dict = {}
            for f in frame_set:
                subs_dict.update(f.variable_map(frame))
            return expr.subs(subs_dict)
        return expr

