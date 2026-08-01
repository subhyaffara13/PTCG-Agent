
def random_insert(circuit, choices, seed=None):
    """Insert a circuit into another quantum circuit.

    Explanation
    ===========

    random_insert randomly chooses a location in the circuit to insert
    a randomly selected circuit from amongst the given choices.

    Parameters
    ==========

    circuit : Gate tuple or Mul
        A tuple or Mul of Gates representing a quantum circuit
    choices : list
        Set of circuit choices
    seed : int or list
        seed used for _randrange; to override the random selections, give
        a list two integers, [i, j] where i is the circuit location where
        choice[j] will be inserted.

    Notes
    =====

    Indices for insertion should be [0, n] if n is the length of the
    circuit.
    """
    from sympy.core.random import _randrange

    if not choices:
        return circuit

    if isinstance(circuit, Mul):
        circuit = circuit.args

    # get the location in the circuit and the element to insert from choices
    randrange = _randrange(seed)
    loc = randrange(len(circuit) + 1)
    choice = choices[randrange(len(choices))]

    circuit = list(circuit)
    circuit[loc: loc] = choice
    return tuple(circuit)

