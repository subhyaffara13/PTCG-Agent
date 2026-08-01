
def test_qasm_3q():
    q = Qasm('qubit q0', 'qubit q1', 'qubit q2', 'toffoli q2,q1,q0')
    assert q.get_circuit() == CGateS((0,1),X(2))

