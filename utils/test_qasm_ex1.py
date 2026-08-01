
def test_qasm_ex1():
    q = Qasm('qubit q0', 'qubit q1', 'h q0', 'cnot q0,q1')
    assert q.get_circuit() == CNOT(1,0)*H(1)

