
def test_qasm_fixcommand():
    assert fixcommand('foo') == 'foo'
    assert fixcommand('def') == 'qdef'

