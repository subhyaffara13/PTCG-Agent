
def test_pretty_misc_functions():
    assert pretty(LambertW(x)) == 'W(x)'
    assert upretty(LambertW(x)) == 'W(x)'
    assert pretty(LambertW(x, y)) == 'W(x, y)'
    assert upretty(LambertW(x, y)) == 'W(x, y)'
    assert pretty(airyai(x)) == 'Ai(x)'
    assert upretty(airyai(x)) == 'Ai(x)'
    assert pretty(airybi(x)) == 'Bi(x)'
    assert upretty(airybi(x)) == 'Bi(x)'
    assert pretty(airyaiprime(x)) == "Ai'(x)"
    assert upretty(airyaiprime(x)) == "Ai'(x)"
    assert pretty(airybiprime(x)) == "Bi'(x)"
    assert upretty(airybiprime(x)) == "Bi'(x)"
    assert pretty(fresnelc(x)) == 'C(x)'
    assert upretty(fresnelc(x)) == 'C(x)'
    assert pretty(fresnels(x)) == 'S(x)'
    assert upretty(fresnels(x)) == 'S(x)'
    assert pretty(Heaviside(x)) == 'Heaviside(x)'
    assert upretty(Heaviside(x)) == 'θ(x)'
    assert pretty(Heaviside(x, y)) == 'Heaviside(x, y)'
    assert upretty(Heaviside(x, y)) == 'θ(x, y)'
    assert pretty(dirichlet_eta(x)) == 'dirichlet_eta(x)'
    assert upretty(dirichlet_eta(x)) == 'η(x)'

