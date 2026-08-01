
def test_qasm_ex1_methodcalls():
    q = Qasm()
    q.qubit('q_0')
    q.qubit('q_1')
    q.h('q_0')
    q.cnot('q_0', 'q_1')
    assert q.get_circuit() == CNOT(1,0)*H(1)

