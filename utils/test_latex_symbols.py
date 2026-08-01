
def test_latex_symbols():
    Gamma, lmbda, rho = symbols('Gamma, lambda, rho')
    tau, Tau, TAU, taU = symbols('tau, Tau, TAU, taU')
    assert latex(tau) == r"\tau"
    assert latex(Tau) == r"\mathrm{T}"
    assert latex(TAU) == r"\tau"
    assert latex(taU) == r"\tau"
    # Check that all capitalized greek letters are handled explicitly
    capitalized_letters = {l.capitalize() for l in greek_letters_set}
    assert len(capitalized_letters - set(tex_greek_dictionary.keys())) == 0
    assert latex(Gamma + lmbda) == r"\Gamma + \lambda"
    assert latex(Gamma * lmbda) == r"\Gamma \lambda"
    assert latex(Symbol('q1')) == r"q_{1}"
    assert latex(Symbol('q21')) == r"q_{21}"
    assert latex(Symbol('epsilon0')) == r"\epsilon_{0}"
    assert latex(Symbol('omega1')) == r"\omega_{1}"
    assert latex(Symbol('91')) == r"91"
    assert latex(Symbol('alpha_new')) == r"\alpha_{new}"
    assert latex(Symbol('C^orig')) == r"C^{orig}"
    assert latex(Symbol('x^alpha')) == r"x^{\alpha}"
    assert latex(Symbol('beta^alpha')) == r"\beta^{\alpha}"
    assert latex(Symbol('e^Alpha')) == r"e^{\mathrm{A}}"
    assert latex(Symbol('omega_alpha^beta')) == r"\omega^{\beta}_{\alpha}"
    assert latex(Symbol('omega') ** Symbol('beta')) == r"\omega^{\beta}"

