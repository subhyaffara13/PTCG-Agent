
def test_complex_2899():
    a, b = symbols('a,b', real=True)
    for deep in [True, False]:
        for func in [sinh, cosh, tanh, coth]:
            assert func(a).expand(complex=True, deep=deep) == func(a)

