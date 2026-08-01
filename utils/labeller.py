
def labeller(n, symbol='q'):
    """Autogenerate labels for wires of quantum circuits.

    Parameters
    ==========

    n : int
        number of qubits in the circuit.
    symbol : string
        A character string to precede all gate labels. E.g. 'q_0', 'q_1', etc.

    >>> from sympy.physics.quantum.circuitplot import labeller
    >>> labeller(2)
    ['q_1', 'q_0']
    >>> labeller(3,'j')
    ['j_2', 'j_1', 'j_0']
    """
    return ['%s_%d' % (symbol,n-i-1) for i in range(n)]

