
def test_mul_flatten_oo():
    p = symbols('p', positive=True)
    n, m = symbols('n,m', negative=True)
    x_im = symbols('x_im', imaginary=True)
    assert n*oo is -oo
    assert n*m*oo is oo
    assert p*oo is oo
    assert x_im*oo != I*oo  # i could be +/- 3*I -> +/-oo

