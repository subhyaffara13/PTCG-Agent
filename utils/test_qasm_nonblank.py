
def test_qasm_nonblank():
    assert list(nonblank('abcd')) == list('abcd')
    assert list(nonblank('abc ')) == list('abc')

