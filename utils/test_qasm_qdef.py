
def test_qasm_qdef():
    # weaker test condition (str) since we don't have access to the actual class
    q = Qasm("def Q,0,Q",'qubit q0','Q q0')
    assert str(q.get_circuit()) == 'Q(0)'

    q = Qasm("def CQ,1,Q", 'qubit q0', 'qubit q1', 'CQ q0,q1')
    assert str(q.get_circuit()) == 'C((1),Q(0))'

