
def convert_to_real_indices(seq, qubit_map):
    """Returns the circuit with real indices.

    Parameters
    ==========

    seq : tuple, Gate/Integer/tuple or Mul
        A tuple of Gate, Integer, or tuple objects or a Mul
    qubit_map : dict
        A dictionary mapping symbolic indices to real indices.

    Examples
    ========

    Change the symbolic indices to real integers:

    >>> from sympy import symbols
    >>> from sympy.physics.quantum.circuitutils import convert_to_real_indices
    >>> from sympy.physics.quantum.gate import X, Y, H
    >>> i0, i1 = symbols('i:2')
    >>> index_map = {i0 : 0, i1 : 1}
    >>> convert_to_real_indices(X(i0)*Y(i1)*H(i0)*X(i1), index_map)
    (X(0), Y(1), H(0), X(1))
    """

    if isinstance(seq, Mul):
        seq = seq.args

    if not isinstance(qubit_map, dict):
        msg = 'Expected dict for qubit_map, got %r.' % qubit_map
        raise TypeError(msg)

    qubit_map = _sympify_qubit_map(qubit_map)
    real_seq = ()
    for item in seq:
        # Nested items, so recurse
        if isinstance(item, Gate):
            real_item = convert_to_real_indices(item.args, qubit_map)

        elif isinstance(item, (tuple, Tuple)):
            real_item = convert_to_real_indices(item, qubit_map)

        else:
            real_item = qubit_map[item]

        if isinstance(item, Gate):
            real_item = item.__class__(*real_item)

        real_seq = real_seq + (real_item,)

    return real_seq

