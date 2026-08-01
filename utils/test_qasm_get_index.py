
def test_qasm_get_index():
    assert get_index('q0', ['q0', 'q1']) == 1
    assert get_index('q1', ['q0', 'q1']) == 0

