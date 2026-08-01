
def test_qasm_swap():
    q = Qasm('qubit q0', 'qubit q1', 'cnot q0,q1', 'cnot q1,q0', 'cnot q0,q1')
    assert q.get_circuit() == CNOT(1,0)*CNOT(0,1)*CNOT(1,0)

