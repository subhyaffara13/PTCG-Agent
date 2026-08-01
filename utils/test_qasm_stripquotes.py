
def test_qasm_stripquotes():
    assert stripquotes("'S'") == 'S'
    assert stripquotes('"S"') == 'S'
    assert stripquotes('S') == 'S'

