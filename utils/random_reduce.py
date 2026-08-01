
def random_reduce(circuit, gate_ids, seed=None):
    """Shorten the length of a quantum circuit.

    Explanation
    ===========

    random_reduce looks for circuit identities in circuit, randomly chooses
    one to remove, and returns a shorter yet equivalent circuit.  If no
    identities are found, the same circuit is returned.

    Parameters
    ==========

    circuit : Gate tuple of Mul
        A tuple of Gates representing a quantum circuit
    gate_ids : list, GateIdentity
        List of gate identities to find in circuit
    seed : int or list
        seed used for _randrange; to override the random selection, provide a
        list of integers: the elements of gate_ids will be tested in the order
        given by the list

    """
    from sympy.core.random import _randrange

    if not gate_ids:
        return circuit

    if isinstance(circuit, Mul):
        circuit = circuit.args

    ids = flatten_ids(gate_ids)

    # Create the random integer generator with the seed
    randrange = _randrange(seed)

    # Look for an identity in the circuit
    while ids:
        i = randrange(len(ids))
        id = ids.pop(i)
        if find_subcircuit(circuit, id) != -1:
            break
    else:
        # no identity was found
        return circuit

    # return circuit with the identity removed
    return replace_subcircuit(circuit, id)

