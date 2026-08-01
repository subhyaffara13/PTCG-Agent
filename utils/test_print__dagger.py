
def test_print_Dagger():
    x = symbols('x', commutative=False)
    assert mpp.doprint(Dagger(x)) == '<msup><mi>x</mi>&#x2020;</msup>'

