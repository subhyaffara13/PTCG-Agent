
def random_circuit(ngates, nqubits, gate_space=(X, Y, Z, S, T, H, CNOT, SWAP)):
    """Return a random circuit of ngates and nqubits.

    This uses an equally weighted sample of (X, Y, Z, S, T, H, CNOT, SWAP)
    gates.

    Parameters
    ----------
    ngates : int
        The number of gates in the circuit.
    nqubits : int
        The number of qubits in the circuit.
    gate_space : tuple
        A tuple of the gate classes that will be used in the circuit.
        Repeating gate classes multiple times in this tuple will increase
        the frequency they appear in the random circuit.
    """
    qubit_space = range(nqubits)
    result = []
    for i in range(ngates):
        g = random.choice(gate_space)
        if g == CNotGate or g == SwapGate:
            qubits = random.sample(qubit_space, 2)
            g = g(*qubits)
        else:
            qubit = random.choice(qubit_space)
            g = g(qubit)
        result.append(g)
    return Mul(*result)

