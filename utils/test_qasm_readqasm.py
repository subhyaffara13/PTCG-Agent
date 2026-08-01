
def test_qasm_readqasm():
    qasm_lines = """\
    qubit q_0
    qubit q_1
    h q_0
    cnot q_0,q_1
    """
    q = read_qasm(qasm_lines)
    assert q.get_circuit() == CNOT(1,0)*H(1)

