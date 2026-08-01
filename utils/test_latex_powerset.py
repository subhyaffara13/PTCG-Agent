
def test_latex_powerset():
    fset = FiniteSet(1, 2, 3)
    assert latex(PowerSet(fset)) == r'\mathcal{P}\left(\left\{1, 2, 3\right\}\right)'

