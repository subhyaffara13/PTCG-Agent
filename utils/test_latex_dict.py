
def test_latex_dict():
    d = {Rational(1): 1, x**2: 2, x: 3, x**3: 4}
    assert latex(d) == \
        r'\left\{ 1 : 1, \  x : 3, \  x^{2} : 2, \  x^{3} : 4\right\}'
    D = Dict(d)
    assert latex(D) == \
        r'\left\{ 1 : 1, \  x : 3, \  x^{2} : 2, \  x^{3} : 4\right\}'

