
def test_createc():
    Qgate = CreateCGate('Q')
    assert str(Qgate([1],0)) == 'C((1),Q(0))'

