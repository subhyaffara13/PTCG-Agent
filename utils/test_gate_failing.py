
def test_gate_failing():
    a, b, c, d = symbols('a,b,c,d')
    uMat = Matrix([[a, b], [c, d]])
    g = UGate((0,), uMat)
    assert str(g) == 'U(0)'

