
def rr_op(left, right):
    """Perform a RR operation.

    A RR operation multiplies both left and right circuits
    with the dagger of the right circuit's rightmost gate, and
    the dagger is multiplied on the right side of both circuits.

    If a RR is possible, it returns the new gate rule as a
    2-tuple (LHS, RHS), where LHS is the left circuit and
    and RHS is the right circuit of the new rule.
    If a RR is not possible, None is returned.

    Parameters
    ==========

    left : Gate tuple
        The left circuit of a gate rule expression.
    right : Gate tuple
        The right circuit of a gate rule expression.

    Examples
    ========

    Generate a new gate rule using a RR operation:

    >>> from sympy.physics.quantum.identitysearch import rr_op
    >>> from sympy.physics.quantum.gate import X, Y, Z
    >>> x = X(0); y = Y(0); z = Z(0)
    >>> rr_op((x, y), (z,))
    ((X(0), Y(0), Z(0)), ())

    >>> rr_op((x,), (y, z))
    ((X(0), Z(0)), (Y(0),))
    """

    if (len(right) > 0):
        rr_gate = right[len(right) - 1]
        rr_gate_is_unitary = is_scalar_matrix(
            (Dagger(rr_gate), rr_gate), _get_min_qubits(rr_gate), True)

    if (len(right) > 0 and rr_gate_is_unitary):
        # Get the new right side w/o the rightmost gate
        new_right = right[0:len(right) - 1]
        # Add the rightmost gate to the right position on the right side
        new_left = left + (Dagger(rr_gate),)
        # Return the new gate rule
        return (new_left, new_right)

    return None

