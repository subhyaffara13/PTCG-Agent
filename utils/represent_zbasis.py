
def represent_zbasis(controls, targets, target_matrix, nqubits, format='sympy'):
    """Represent a gate with controls, targets and target_matrix.

    This function does the low-level work of representing gates as matrices
    in the standard computational basis (ZGate). Currently, we support two
    main cases:

    1. One target qubit and no control qubits.
    2. One target qubits and multiple control qubits.

    For the base of multiple controls, we use the following expression [1]:

    1_{2**n} + (|1><1|)^{(n-1)} x (target-matrix - 1_{2})

    Parameters
    ----------
    controls : list, tuple
        A sequence of control qubits.
    targets : list, tuple
        A sequence of target qubits.
    target_matrix : sympy.Matrix, numpy.matrix, scipy.sparse
        The matrix form of the transformation to be performed on the target
        qubits.  The format of this matrix must match that passed into
        the `format` argument.
    nqubits : int
        The total number of qubits used for the representation.
    format : str
        The format of the final matrix ('sympy', 'numpy', 'scipy.sparse').

    Examples
    ========

    References
    ----------
    [1] http://www.johnlapeyre.com/qinf/qinf_html/node6.html.
    """
    controls = [int(x) for x in controls]
    targets = [int(x) for x in targets]
    nqubits = int(nqubits)

    # This checks for the format as well.
    op11 = matrix_cache.get_matrix('op11', format)
    eye2 = matrix_cache.get_matrix('eye2', format)

    # Plain single qubit case
    if len(controls) == 0 and len(targets) == 1:
        product = []
        bit = targets[0]
        # Fill product with [I1,Gate,I2] such that the unitaries,
        # I, cause the gate to be applied to the correct Qubit
        if bit != nqubits - 1:
            product.append(matrix_eye(2**(nqubits - bit - 1), format=format))
        product.append(target_matrix)
        if bit != 0:
            product.append(matrix_eye(2**bit, format=format))
        return matrix_tensor_product(*product)

    # Single target, multiple controls.
    elif len(targets) == 1 and len(controls) >= 1:
        target = targets[0]

        # Build the non-trivial part.
        product2 = []
        for i in range(nqubits):
            product2.append(matrix_eye(2, format=format))
        for control in controls:
            product2[nqubits - 1 - control] = op11
        product2[nqubits - 1 - target] = target_matrix - eye2

        return matrix_eye(2**nqubits, format=format) + \
            matrix_tensor_product(*product2)

    # Multi-target, multi-control is not yet implemented.
    else:
        raise NotImplementedError(
            'The representation of multi-target, multi-control gates '
            'is not implemented.'
        )

