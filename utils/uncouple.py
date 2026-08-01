
def uncouple(expr, jn=None, jcoupling_list=None):
    """ Uncouple a coupled spin state

    Gives the uncoupled representation of a coupled spin state. Arguments must
    be either a spin state that is a subclass of CoupledSpinState or a spin
    state that is a subclass of SpinState and an array giving the j values
    of the spaces that are to be coupled

    Parameters
    ==========

    expr : Expr
        The expression containing states that are to be coupled. If the states
        are a subclass of SpinState, the ``jn`` and ``jcoupling`` parameters
        must be defined. If the states are a subclass of CoupledSpinState,
        ``jn`` and ``jcoupling`` will be taken from the state.

    jn : list or tuple
        The list of the j-values that are coupled. If state is a
        CoupledSpinState, this parameter is ignored. This must be defined if
        state is not a subclass of CoupledSpinState. The syntax of this
        parameter is the same as the ``jn`` parameter of JzKetCoupled.

    jcoupling_list : list or tuple
        The list defining how the j-values are coupled together. If state is a
        CoupledSpinState, this parameter is ignored. This must be defined if
        state is not a subclass of CoupledSpinState. The syntax of this
        parameter is the same as the ``jcoupling`` parameter of JzKetCoupled.

    Examples
    ========

    Uncouple a numerical state using a CoupledSpinState state:

        >>> from sympy.physics.quantum.spin import JzKetCoupled, uncouple
        >>> from sympy import S
        >>> uncouple(JzKetCoupled(1, 0, (S(1)/2, S(1)/2)))
        sqrt(2)*|1/2,-1/2>x|1/2,1/2>/2 + sqrt(2)*|1/2,1/2>x|1/2,-1/2>/2

    Perform the same calculation using a SpinState state:

        >>> from sympy.physics.quantum.spin import JzKet
        >>> uncouple(JzKet(1, 0), (S(1)/2, S(1)/2))
        sqrt(2)*|1/2,-1/2>x|1/2,1/2>/2 + sqrt(2)*|1/2,1/2>x|1/2,-1/2>/2

    Uncouple a numerical state of three coupled spaces using a CoupledSpinState state:

        >>> uncouple(JzKetCoupled(1, 1, (1, 1, 1), ((1,3,1),(1,2,1)) ))
        |1,-1>x|1,1>x|1,1>/2 - |1,0>x|1,0>x|1,1>/2 + |1,1>x|1,0>x|1,0>/2 - |1,1>x|1,1>x|1,-1>/2

    Perform the same calculation using a SpinState state:

        >>> uncouple(JzKet(1, 1), (1, 1, 1), ((1,3,1),(1,2,1)) )
        |1,-1>x|1,1>x|1,1>/2 - |1,0>x|1,0>x|1,1>/2 + |1,1>x|1,0>x|1,0>/2 - |1,1>x|1,1>x|1,-1>/2

    Uncouple a symbolic state using a CoupledSpinState state:

        >>> from sympy import symbols
        >>> j,m,j1,j2 = symbols('j m j1 j2')
        >>> uncouple(JzKetCoupled(j, m, (j1, j2)))
        Sum(CG(j1, m1, j2, m2, j, m)*|j1,m1>x|j2,m2>, (m1, -j1, j1), (m2, -j2, j2))

    Perform the same calculation using a SpinState state

        >>> uncouple(JzKet(j, m), (j1, j2))
        Sum(CG(j1, m1, j2, m2, j, m)*|j1,m1>x|j2,m2>, (m1, -j1, j1), (m2, -j2, j2))

    """
    a = expr.atoms(SpinState)
    for state in a:
        expr = expr.subs(state, _uncouple(state, jn, jcoupling_list))
    return expr

