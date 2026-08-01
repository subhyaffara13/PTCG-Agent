
def test_qasm_1q():
    for symbol, gate in [('x', X), ('z', Z), ('h', H), ('s', S), ('t', T), ('measure', Mz)]:
        q = Qasm('qubit q_0', '%s q_0' % symbol)
        assert q.get_circuit() == gate(0)

