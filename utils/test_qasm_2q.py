
def test_qasm_2q():
    for symbol, gate in [('cnot', CNOT), ('swap', SWAP), ('cphase', CPHASE)]:
        q = Qasm('qubit q_0', 'qubit q_1', '%s q_0,q_1' % symbol)
        assert q.get_circuit() == gate(1,0)

