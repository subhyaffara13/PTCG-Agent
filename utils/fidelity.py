
def fidelity(state1, state2):
    """ Computes the fidelity [1]_ between two quantum states

    The arguments provided to this function should be a square matrix or a
    Density object. If it is a square matrix, it is assumed to be diagonalizable.

    Parameters
    ==========

    state1, state2 : a density matrix or Matrix


    Examples
    ========

    >>> from sympy import S, sqrt
    >>> from sympy.physics.quantum.dagger import Dagger
    >>> from sympy.physics.quantum.spin import JzKet
    >>> from sympy.physics.quantum.density import fidelity
    >>> from sympy.physics.quantum.represent import represent
    >>>
    >>> up = JzKet(S(1)/2,S(1)/2)
    >>> down = JzKet(S(1)/2,-S(1)/2)
    >>> amp = 1/sqrt(2)
    >>> updown = (amp*up) + (amp*down)
    >>>
    >>> # represent turns Kets into matrices
    >>> up_dm = represent(up*Dagger(up))
    >>> down_dm = represent(down*Dagger(down))
    >>> updown_dm = represent(updown*Dagger(updown))
    >>>
    >>> fidelity(up_dm, up_dm)
    1
    >>> fidelity(up_dm, down_dm) #orthogonal states
    0
    >>> fidelity(up_dm, updown_dm).evalf().round(3)
    0.707

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Fidelity_of_quantum_states

    """
    state1 = represent(state1) if isinstance(state1, Density) else state1
    state2 = represent(state2) if isinstance(state2, Density) else state2

    if not isinstance(state1, Matrix) or not isinstance(state2, Matrix):
        raise ValueError("state1 and state2 must be of type Density or Matrix "
                         "received type=%s for state1 and type=%s for state2" %
                         (type(state1), type(state2)))

    if state1.shape != state2.shape and state1.is_square:
        raise ValueError("The dimensions of both args should be equal and the "
                         "matrix obtained should be a square matrix")

    sqrt_state1 = state1**S.Half
    return Tr((sqrt_state1*state2*sqrt_state1)**S.Half).doit()

