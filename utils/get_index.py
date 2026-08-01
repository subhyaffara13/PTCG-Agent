
def get_index(target, labels):
    """Get qubit labels from the rest of the line,and return indices

    >>> from sympy.physics.quantum.qasm import get_index
    >>> get_index('q0', ['q0', 'q1'])
    1
    >>> get_index('q1', ['q0', 'q1'])
    0
    """
    nq = len(labels)
    return flip_index(labels.index(target), nq)

