
def test_qubit():
    q1 = Qubit('0101')
    q2 = IntQubit(8)
    assert str(q1) == '|0101>'
    assert pretty(q1) == '|0101>'
    assert upretty(q1) == '❘0101⟩'
    assert latex(q1) == r'{\left|0101\right\rangle }'
    sT(q1, "Qubit(Integer(0),Integer(1),Integer(0),Integer(1))")
    assert str(q2) == '|8>'
    assert pretty(q2) == '|8>'
    assert upretty(q2) == '❘8⟩'
    assert latex(q2) == r'{\left|8\right\rangle }'
    sT(q2, "IntQubit(8)")

