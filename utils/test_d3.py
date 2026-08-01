
def test_D3():
    assert exp(pi*sqrt(163)).evalf(50).num.ae(262537412640768744)

