
def test_latex_fresnel():
    from sympy.functions.special.error_functions import (fresnels, fresnelc)
    from sympy.abc import z
    assert latex(fresnels(z)) == r'S\left(z\right)'
    assert latex(fresnelc(z)) == r'C\left(z\right)'
    assert latex(fresnels(z)**2) == r'S^{2}\left(z\right)'
    assert latex(fresnelc(z)**2) == r'C^{2}\left(z\right)'

