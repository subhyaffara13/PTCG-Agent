
def test_Poly_mixed_operations():
    p = Poly(x, x)
    with warns_deprecated_sympy():
        p * exp(x)
    with warns_deprecated_sympy():
        p + exp(x)
    with warns_deprecated_sympy():
        p - exp(x)

