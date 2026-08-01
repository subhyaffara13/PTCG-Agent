
def test_airy_base():
    z = Symbol('z')
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)

    assert conjugate(airyai(z)) == airyai(conjugate(z))
    assert airyai(x).is_extended_real

    assert airyai(x+I*y).as_real_imag() == (
            airyai(x - I*y)/2 + airyai(x + I*y)/2,
            I*(airyai(x - I*y) - airyai(x + I*y))/2)

