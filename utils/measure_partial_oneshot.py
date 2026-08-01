
def measure_partial_oneshot(qubit, bits, format='sympy'):
    """Perform a partial oneshot measurement on the specified qubits.

    A oneshot measurement is equivalent to performing a measurement on a
    quantum system. This type of measurement does not return the probabilities
    like an ensemble measurement does, but rather returns *one* of the
    possible resulting states. The exact state that is returned is determined
    by picking a state randomly according to the ensemble probabilities.

    Parameters
    ----------
    qubits : Qubit
        The qubit to measure.  This can be any Qubit or a linear combination
        of them.
    bits : tuple
        The qubits to measure.
    format : str
        The format of the intermediate matrices to use. Possible values are
        ('sympy','numpy','scipy.sparse'). Currently only 'sympy' is
        implemented.

    Returns
    -------
    result : Qubit
        The qubit that the system collapsed to upon measurement.
    """
    import random
    m = qubit_to_matrix(qubit, format)

    if format == 'sympy':
        m = m.normalized()
        possible_outcomes = _get_possible_outcomes(m, bits)

        # Form output from function
        random_number = random.random()
        total_prob = 0
        for outcome in possible_outcomes:
            # Calculate probability of finding the specified bits
            # with given values
            total_prob += (outcome.H*outcome)[0]
            if total_prob >= random_number:
                return matrix_to_qubit(outcome.normalized())
    else:
        raise NotImplementedError(
            "This function cannot handle non-SymPy matrix formats yet"
        )

