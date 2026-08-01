
def random_identity_search(gate_list, numgates, nqubits):
    """Randomly selects numgates from gate_list and checks if it is
    a gate identity.

    If the circuit is a gate identity, the circuit is returned;
    Otherwise, None is returned.
    """

    gate_size = len(gate_list)
    circuit = ()

    for i in range(numgates):
        next_gate = gate_list[randint(0, gate_size - 1)]
        circuit = circuit + (next_gate,)

    is_scalar = is_scalar_matrix(circuit, nqubits, False)

    return circuit if is_scalar else None

