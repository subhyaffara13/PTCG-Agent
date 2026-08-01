
def test_latex_mathieu():
    assert latex(mathieuc(x, y, z)) == r"C\left(x, y, z\right)"
    assert latex(mathieus(x, y, z)) == r"S\left(x, y, z\right)"
    assert latex(mathieuc(x, y, z)**2) == r"C\left(x, y, z\right)^{2}"
    assert latex(mathieus(x, y, z)**2) == r"S\left(x, y, z\right)^{2}"
    assert latex(mathieucprime(x, y, z)) == r"C^{\prime}\left(x, y, z\right)"
    assert latex(mathieusprime(x, y, z)) == r"S^{\prime}\left(x, y, z\right)"
    assert latex(mathieucprime(x, y, z)**2) == r"C^{\prime}\left(x, y, z\right)^{2}"
    assert latex(mathieusprime(x, y, z)**2) == r"S^{\prime}\left(x, y, z\right)^{2}"

