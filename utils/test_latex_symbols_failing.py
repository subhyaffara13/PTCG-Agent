
def test_latex_symbols_failing():
    rho, mass, volume = symbols('rho, mass, volume')
    assert latex(
        volume * rho == mass) == r"\rho \mathrm{volume} = \mathrm{mass}"
    assert latex(volume / mass * rho == 1) == \
        r"\rho \mathrm{volume} {\mathrm{mass}}^{(-1)} = 1"
    assert latex(mass**3 * volume**3) == \
        r"{\mathrm{mass}}^{3} \cdot {\mathrm{volume}}^{3}"

