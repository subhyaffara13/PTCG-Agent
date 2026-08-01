
def test_qasm_fullsplit():
    assert fullsplit('g q0,q1,q2,  q3') == ('g', ['q0', 'q1', 'q2', 'q3'])

