
def test_latex_LeviCivita():
    assert latex(LeviCivita(x, y, z)) == r"\varepsilon_{x y z}"
    assert latex(LeviCivita(x, y, z)**2) == \
        r"\left(\varepsilon_{x y z}\right)^{2}"
    assert latex(LeviCivita(x, y, z + 1)) == r"\varepsilon_{x, y, z + 1}"
    assert latex(LeviCivita(x, y + 1, z)) == r"\varepsilon_{x, y + 1, z}"
    assert latex(LeviCivita(x + 1, y, z)) == r"\varepsilon_{x + 1, y, z}"

