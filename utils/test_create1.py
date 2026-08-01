
def test_create1():
    Qgate = CreateOneQubitGate('Q')
    assert str(Qgate(0)) == 'Q(0)'

