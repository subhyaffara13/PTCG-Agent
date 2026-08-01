
def test_latex_Heaviside():
    assert latex(Heaviside(x)) == r"\theta\left(x\right)"
    assert latex(Heaviside(x)**2) == r"\left(\theta\left(x\right)\right)^{2}"

