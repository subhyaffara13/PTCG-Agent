
def test_grover_iteration_2():
    numqubits = 4
    basis_states = superposition_basis(numqubits)
    v = OracleGate(numqubits, return_one_on_two)
    # After (pi/4)sqrt(pow(2, n)), IntQubit(2) should have highest prob
    # In this case, after around pi times (3 or 4)
    iterated = grover_iteration(basis_states, v)
    iterated = qapply(iterated)
    iterated = grover_iteration(iterated, v)
    iterated = qapply(iterated)
    iterated = grover_iteration(iterated, v)
    iterated = qapply(iterated)
    # In this case, probability was highest after 3 iterations
    # Probability of Qubit('0010') was 251/256 (3) vs 781/1024 (4)
    # Ask about measurement
    expected = (-13*basis_states)/64 + 264*IntQubit(2, numqubits)/256
    assert qapply(expected) == iterated

