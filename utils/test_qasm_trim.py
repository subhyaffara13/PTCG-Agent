
def test_qasm_trim():
    assert trim('nothing happens here') == 'nothing happens here'
    assert trim("Something #happens here") == "Something "

