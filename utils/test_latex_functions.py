
def test_latex_functions():
    assert latex(exp(x)) == r"e^{x}"
    assert latex(exp(1) + exp(2)) == r"e + e^{2}"

    f = Function('f')
    assert latex(f(x)) == r'f{\left(x \right)}'
    assert latex(f) == r'f'

    g = Function('g')
    assert latex(g(x, y)) == r'g{\left(x,y \right)}'
    assert latex(g) == r'g'

    h = Function('h')
    assert latex(h(x, y, z)) == r'h{\left(x,y,z \right)}'
    assert latex(h) == r'h'

    Li = Function('Li')
    assert latex(Li) == r'\operatorname{Li}'
    assert latex(Li(x)) == r'\operatorname{Li}{\left(x \right)}'

    mybeta = Function('beta')
    # not to be confused with the beta function
    assert latex(mybeta(x, y, z)) == r"\beta{\left(x,y,z \right)}"
    assert latex(beta(x, y)) == r'\operatorname{B}\left(x, y\right)'
    assert latex(beta(x, evaluate=False)) == r'\operatorname{B}\left(x, x\right)'
    assert latex(beta(x, y)**2) == r'\operatorname{B}^{2}\left(x, y\right)'
    assert latex(mybeta(x)) == r"\beta{\left(x \right)}"
    assert latex(mybeta) == r"\beta"

    g = Function('gamma')
    # not to be confused with the gamma function
    assert latex(g(x, y, z)) == r"\gamma{\left(x,y,z \right)}"
    assert latex(g(x)) == r"\gamma{\left(x \right)}"
    assert latex(g) == r"\gamma"

    a_1 = Function('a_1')
    assert latex(a_1) == r"a_{1}"
    assert latex(a_1(x)) == r"a_{1}{\left(x \right)}"
    assert latex(Function('a_1')) == r"a_{1}"

    # Issue #16925
    # multi letter function names
    # > simple
    assert latex(Function('ab')) == r"\operatorname{ab}"
    assert latex(Function('ab1')) == r"\operatorname{ab}_{1}"
    assert latex(Function('ab12')) == r"\operatorname{ab}_{12}"
    assert latex(Function('ab_1')) == r"\operatorname{ab}_{1}"
    assert latex(Function('ab_12')) == r"\operatorname{ab}_{12}"
    assert latex(Function('ab_c')) == r"\operatorname{ab}_{c}"
    assert latex(Function('ab_cd')) == r"\operatorname{ab}_{cd}"
    # > with argument
    assert latex(Function('ab')(Symbol('x'))) == r"\operatorname{ab}{\left(x \right)}"
    assert latex(Function('ab1')(Symbol('x'))) == r"\operatorname{ab}_{1}{\left(x \right)}"
    assert latex(Function('ab12')(Symbol('x'))) == r"\operatorname{ab}_{12}{\left(x \right)}"
    assert latex(Function('ab_1')(Symbol('x'))) == r"\operatorname{ab}_{1}{\left(x \right)}"
    assert latex(Function('ab_c')(Symbol('x'))) == r"\operatorname{ab}_{c}{\left(x \right)}"
    assert latex(Function('ab_cd')(Symbol('x'))) == r"\operatorname{ab}_{cd}{\left(x \right)}"

    # > with power
    #   does not work on functions without brackets

    # > with argument and power combined
    assert latex(Function('ab')()**2) == r"\operatorname{ab}^{2}{\left( \right)}"
    assert latex(Function('ab1')()**2) == r"\operatorname{ab}_{1}^{2}{\left( \right)}"
    assert latex(Function('ab12')()**2) == r"\operatorname{ab}_{12}^{2}{\left( \right)}"
    assert latex(Function('ab_1')()**2) == r"\operatorname{ab}_{1}^{2}{\left( \right)}"
    assert latex(Function('ab_12')()**2) == r"\operatorname{ab}_{12}^{2}{\left( \right)}"
    assert latex(Function('ab')(Symbol('x'))**2) == r"\operatorname{ab}^{2}{\left(x \right)}"
    assert latex(Function('ab1')(Symbol('x'))**2) == r"\operatorname{ab}_{1}^{2}{\left(x \right)}"
    assert latex(Function('ab12')(Symbol('x'))**2) == r"\operatorname{ab}_{12}^{2}{\left(x \right)}"
    assert latex(Function('ab_1')(Symbol('x'))**2) == r"\operatorname{ab}_{1}^{2}{\left(x \right)}"
    assert latex(Function('ab_12')(Symbol('x'))**2) == \
        r"\operatorname{ab}_{12}^{2}{\left(x \right)}"

    # single letter function names
    # > simple
    assert latex(Function('a')) == r"a"
    assert latex(Function('a1')) == r"a_{1}"
    assert latex(Function('a12')) == r"a_{12}"
    assert latex(Function('a_1')) == r"a_{1}"
    assert latex(Function('a_12')) == r"a_{12}"

    # > with argument
    assert latex(Function('a')()) == r"a{\left( \right)}"
    assert latex(Function('a1')()) == r"a_{1}{\left( \right)}"
    assert latex(Function('a12')()) == r"a_{12}{\left( \right)}"
    assert latex(Function('a_1')()) == r"a_{1}{\left( \right)}"
    assert latex(Function('a_12')()) == r"a_{12}{\left( \right)}"

    # > with power
    #   does not work on functions without brackets

    # > with argument and power combined
    assert latex(Function('a')()**2) == r"a^{2}{\left( \right)}"
    assert latex(Function('a1')()**2) == r"a_{1}^{2}{\left( \right)}"
    assert latex(Function('a12')()**2) == r"a_{12}^{2}{\left( \right)}"
    assert latex(Function('a_1')()**2) == r"a_{1}^{2}{\left( \right)}"
    assert latex(Function('a_12')()**2) == r"a_{12}^{2}{\left( \right)}"
    assert latex(Function('a')(Symbol('x'))**2) == r"a^{2}{\left(x \right)}"
    assert latex(Function('a1')(Symbol('x'))**2) == r"a_{1}^{2}{\left(x \right)}"
    assert latex(Function('a12')(Symbol('x'))**2) == r"a_{12}^{2}{\left(x \right)}"
    assert latex(Function('a_1')(Symbol('x'))**2) == r"a_{1}^{2}{\left(x \right)}"
    assert latex(Function('a_12')(Symbol('x'))**2) == r"a_{12}^{2}{\left(x \right)}"

    assert latex(Function('a')()**32) == r"a^{32}{\left( \right)}"
    assert latex(Function('a1')()**32) == r"a_{1}^{32}{\left( \right)}"
    assert latex(Function('a12')()**32) == r"a_{12}^{32}{\left( \right)}"
    assert latex(Function('a_1')()**32) == r"a_{1}^{32}{\left( \right)}"
    assert latex(Function('a_12')()**32) == r"a_{12}^{32}{\left( \right)}"
    assert latex(Function('a')(Symbol('x'))**32) == r"a^{32}{\left(x \right)}"
    assert latex(Function('a1')(Symbol('x'))**32) == r"a_{1}^{32}{\left(x \right)}"
    assert latex(Function('a12')(Symbol('x'))**32) == r"a_{12}^{32}{\left(x \right)}"
    assert latex(Function('a_1')(Symbol('x'))**32) == r"a_{1}^{32}{\left(x \right)}"
    assert latex(Function('a_12')(Symbol('x'))**32) == r"a_{12}^{32}{\left(x \right)}"

    assert latex(Function('a')()**a) == r"a^{a}{\left( \right)}"
    assert latex(Function('a1')()**a) == r"a_{1}^{a}{\left( \right)}"
    assert latex(Function('a12')()**a) == r"a_{12}^{a}{\left( \right)}"
    assert latex(Function('a_1')()**a) == r"a_{1}^{a}{\left( \right)}"
    assert latex(Function('a_12')()**a) == r"a_{12}^{a}{\left( \right)}"
    assert latex(Function('a')(Symbol('x'))**a) == r"a^{a}{\left(x \right)}"
    assert latex(Function('a1')(Symbol('x'))**a) == r"a_{1}^{a}{\left(x \right)}"
    assert latex(Function('a12')(Symbol('x'))**a) == r"a_{12}^{a}{\left(x \right)}"
    assert latex(Function('a_1')(Symbol('x'))**a) == r"a_{1}^{a}{\left(x \right)}"
    assert latex(Function('a_12')(Symbol('x'))**a) == r"a_{12}^{a}{\left(x \right)}"

    ab = Symbol('ab')
    assert latex(Function('a')()**ab) == r"a^{ab}{\left( \right)}"
    assert latex(Function('a1')()**ab) == r"a_{1}^{ab}{\left( \right)}"
    assert latex(Function('a12')()**ab) == r"a_{12}^{ab}{\left( \right)}"
    assert latex(Function('a_1')()**ab) == r"a_{1}^{ab}{\left( \right)}"
    assert latex(Function('a_12')()**ab) == r"a_{12}^{ab}{\left( \right)}"
    assert latex(Function('a')(Symbol('x'))**ab) == r"a^{ab}{\left(x \right)}"
    assert latex(Function('a1')(Symbol('x'))**ab) == r"a_{1}^{ab}{\left(x \right)}"
    assert latex(Function('a12')(Symbol('x'))**ab) == r"a_{12}^{ab}{\left(x \right)}"
    assert latex(Function('a_1')(Symbol('x'))**ab) == r"a_{1}^{ab}{\left(x \right)}"
    assert latex(Function('a_12')(Symbol('x'))**ab) == r"a_{12}^{ab}{\left(x \right)}"

    assert latex(Function('a^12')(x)) == R"a^{12}{\left(x \right)}"
    assert latex(Function('a^12')(x) ** ab) == R"\left(a^{12}\right)^{ab}{\left(x \right)}"
    assert latex(Function('a__12')(x)) == R"a^{12}{\left(x \right)}"
    assert latex(Function('a__12')(x) ** ab) == R"\left(a^{12}\right)^{ab}{\left(x \right)}"
    assert latex(Function('a_1__1_2')(x)) == R"a^{1}_{1 2}{\left(x \right)}"

    # issue 5868
    omega1 = Function('omega1')
    assert latex(omega1) == r"\omega_{1}"
    assert latex(omega1(x)) == r"\omega_{1}{\left(x \right)}"

    assert latex(sin(x)) == r"\sin{\left(x \right)}"
    assert latex(sin(x), fold_func_brackets=True) == r"\sin {x}"
    assert latex(sin(2*x**2), fold_func_brackets=True) == \
        r"\sin {2 x^{2}}"
    assert latex(sin(x**2), fold_func_brackets=True) == \
        r"\sin {x^{2}}"

    assert latex(asin(x)**2) == r"\operatorname{asin}^{2}{\left(x \right)}"
    assert latex(asin(x)**2, inv_trig_style="full") == \
        r"\arcsin^{2}{\left(x \right)}"
    assert latex(asin(x)**2, inv_trig_style="power") == \
        r"\sin^{-1}{\left(x \right)}^{2}"
    assert latex(asin(x**2), inv_trig_style="power",
                 fold_func_brackets=True) == \
        r"\sin^{-1} {x^{2}}"
    assert latex(acsc(x), inv_trig_style="full") == \
        r"\operatorname{arccsc}{\left(x \right)}"
    assert latex(asinh(x), inv_trig_style="full") == \
        r"\operatorname{arsinh}{\left(x \right)}"

    assert latex(factorial(k)) == r"k!"
    assert latex(factorial(-k)) == r"\left(- k\right)!"
    assert latex(factorial(k)**2) == r"k!^{2}"

    assert latex(subfactorial(k)) == r"!k"
    assert latex(subfactorial(-k)) == r"!\left(- k\right)"
    assert latex(subfactorial(k)**2) == r"\left(!k\right)^{2}"

    assert latex(factorial2(k)) == r"k!!"
    assert latex(factorial2(-k)) == r"\left(- k\right)!!"
    assert latex(factorial2(k)**2) == r"k!!^{2}"

    assert latex(binomial(2, k)) == r"{\binom{2}{k}}"
    assert latex(binomial(2, k)**2) == r"{\binom{2}{k}}^{2}"

    assert latex(FallingFactorial(3, k)) == r"{\left(3\right)}_{k}"
    assert latex(RisingFactorial(3, k)) == r"{3}^{\left(k\right)}"

    assert latex(floor(x)) == r"\left\lfloor{x}\right\rfloor"
    assert latex(ceiling(x)) == r"\left\lceil{x}\right\rceil"
    assert latex(frac(x)) == r"\operatorname{frac}{\left(x\right)}"
    assert latex(floor(x)**2) == r"\left\lfloor{x}\right\rfloor^{2}"
    assert latex(ceiling(x)**2) == r"\left\lceil{x}\right\rceil^{2}"
    assert latex(frac(x)**2) == r"\operatorname{frac}{\left(x\right)}^{2}"

    assert latex(Min(x, 2, x**3)) == r"\min\left(2, x, x^{3}\right)"
    assert latex(Min(x, y)**2) == r"\min\left(x, y\right)^{2}"
    assert latex(Max(x, 2, x**3)) == r"\max\left(2, x, x^{3}\right)"
    assert latex(Max(x, y)**2) == r"\max\left(x, y\right)^{2}"
    assert latex(Abs(x)) == r"\left|{x}\right|"
    assert latex(Abs(x)**2) == r"\left|{x}\right|^{2}"
    assert latex(re(x)) == r"\operatorname{re}{\left(x\right)}"
    assert latex(re(x + y)) == \
        r"\operatorname{re}{\left(x\right)} + \operatorname{re}{\left(y\right)}"
    assert latex(im(x)) == r"\operatorname{im}{\left(x\right)}"
    assert latex(conjugate(x)) == r"\overline{x}"
    assert latex(conjugate(x)**2) == r"\overline{x}^{2}"
    assert latex(conjugate(x**2)) == r"\overline{x}^{2}"
    assert latex(gamma(x)) == r"\Gamma\left(x\right)"
    w = Wild('w')
    assert latex(gamma(w)) == r"\Gamma\left(w\right)"
    assert latex(Order(x)) == r"O\left(x\right)"
    assert latex(Order(x, x)) == r"O\left(x\right)"
    assert latex(Order(x, (x, 0))) == r"O\left(x\right)"
    assert latex(Order(x, (x, oo))) == r"O\left(x; x\rightarrow \infty\right)"
    assert latex(Order(x - y, (x, y))) == \
        r"O\left(x - y; x\rightarrow y\right)"
    assert latex(Order(x, x, y)) == \
        r"O\left(x; \left( x, \  y\right)\rightarrow \left( 0, \  0\right)\right)"
    assert latex(Order(x, x, y)) == \
        r"O\left(x; \left( x, \  y\right)\rightarrow \left( 0, \  0\right)\right)"
    assert latex(Order(x, (x, oo), (y, oo))) == \
        r"O\left(x; \left( x, \  y\right)\rightarrow \left( \infty, \  \infty\right)\right)"
    assert latex(lowergamma(x, y)) == r'\gamma\left(x, y\right)'
    assert latex(lowergamma(x, y)**2) == r'\gamma^{2}\left(x, y\right)'
    assert latex(uppergamma(x, y)) == r'\Gamma\left(x, y\right)'
    assert latex(uppergamma(x, y)**2) == r'\Gamma^{2}\left(x, y\right)'

    assert latex(cot(x)) == r'\cot{\left(x \right)}'
    assert latex(coth(x)) == r'\coth{\left(x \right)}'
    assert latex(re(x)) == r'\operatorname{re}{\left(x\right)}'
    assert latex(im(x)) == r'\operatorname{im}{\left(x\right)}'
    assert latex(root(x, y)) == r'x^{\frac{1}{y}}'
    assert latex(arg(x)) == r'\arg{\left(x \right)}'

    assert latex(zeta(x)) == r"\zeta\left(x\right)"
    assert latex(zeta(x)**2) == r"\zeta^{2}\left(x\right)"
    assert latex(zeta(x, y)) == r"\zeta\left(x, y\right)"
    assert latex(zeta(x, y)**2) == r"\zeta^{2}\left(x, y\right)"
    assert latex(dirichlet_eta(x)) == r"\eta\left(x\right)"
    assert latex(dirichlet_eta(x)**2) == r"\eta^{2}\left(x\right)"
    assert latex(polylog(x, y)) == r"\operatorname{Li}_{x}\left(y\right)"
    assert latex(
        polylog(x, y)**2) == r"\operatorname{Li}_{x}^{2}\left(y\right)"
    assert latex(lerchphi(x, y, n)) == r"\Phi\left(x, y, n\right)"
    assert latex(lerchphi(x, y, n)**2) == r"\Phi^{2}\left(x, y, n\right)"
    assert latex(stieltjes(x)) == r"\gamma_{x}"
    assert latex(stieltjes(x)**2) == r"\gamma_{x}^{2}"
    assert latex(stieltjes(x, y)) == r"\gamma_{x}\left(y\right)"
    assert latex(stieltjes(x, y)**2) == r"\gamma_{x}\left(y\right)^{2}"

    assert latex(elliptic_k(z)) == r"K\left(z\right)"
    assert latex(elliptic_k(z)**2) == r"K^{2}\left(z\right)"
    assert latex(elliptic_f(x, y)) == r"F\left(x\middle| y\right)"
    assert latex(elliptic_f(x, y)**2) == r"F^{2}\left(x\middle| y\right)"
    assert latex(elliptic_e(x, y)) == r"E\left(x\middle| y\right)"
    assert latex(elliptic_e(x, y)**2) == r"E^{2}\left(x\middle| y\right)"
    assert latex(elliptic_e(z)) == r"E\left(z\right)"
    assert latex(elliptic_e(z)**2) == r"E^{2}\left(z\right)"
    assert latex(elliptic_pi(x, y, z)) == r"\Pi\left(x; y\middle| z\right)"
    assert latex(elliptic_pi(x, y, z)**2) == \
        r"\Pi^{2}\left(x; y\middle| z\right)"
    assert latex(elliptic_pi(x, y)) == r"\Pi\left(x\middle| y\right)"
    assert latex(elliptic_pi(x, y)**2) == r"\Pi^{2}\left(x\middle| y\right)"

    assert latex(Ei(x)) == r'\operatorname{Ei}{\left(x \right)}'
    assert latex(Ei(x)**2) == r'\operatorname{Ei}^{2}{\left(x \right)}'
    assert latex(expint(x, y)) == r'\operatorname{E}_{x}\left(y\right)'
    assert latex(expint(x, y)**2) == r'\operatorname{E}_{x}^{2}\left(y\right)'
    assert latex(Shi(x)**2) == r'\operatorname{Shi}^{2}{\left(x \right)}'
    assert latex(Si(x)**2) == r'\operatorname{Si}^{2}{\left(x \right)}'
    assert latex(Ci(x)**2) == r'\operatorname{Ci}^{2}{\left(x \right)}'
    assert latex(Chi(x)**2) == r'\operatorname{Chi}^{2}\left(x\right)'
    assert latex(Chi(x)) == r'\operatorname{Chi}\left(x\right)'
    assert latex(jacobi(n, a, b, x)) == \
        r'P_{n}^{\left(a,b\right)}\left(x\right)'
    assert latex(jacobi(n, a, b, x)**2) == \
        r'\left(P_{n}^{\left(a,b\right)}\left(x\right)\right)^{2}'
    assert latex(gegenbauer(n, a, x)) == \
        r'C_{n}^{\left(a\right)}\left(x\right)'
    assert latex(gegenbauer(n, a, x)**2) == \
        r'\left(C_{n}^{\left(a\right)}\left(x\right)\right)^{2}'
    assert latex(chebyshevt(n, x)) == r'T_{n}\left(x\right)'
    assert latex(chebyshevt(n, x)**2) == \
        r'\left(T_{n}\left(x\right)\right)^{2}'
    assert latex(chebyshevu(n, x)) == r'U_{n}\left(x\right)'
    assert latex(chebyshevu(n, x)**2) == \
        r'\left(U_{n}\left(x\right)\right)^{2}'
    assert latex(legendre(n, x)) == r'P_{n}\left(x\right)'
    assert latex(legendre(n, x)**2) == r'\left(P_{n}\left(x\right)\right)^{2}'
    assert latex(assoc_legendre(n, a, x)) == \
        r'P_{n}^{\left(a\right)}\left(x\right)'
    assert latex(assoc_legendre(n, a, x)**2) == \
        r'\left(P_{n}^{\left(a\right)}\left(x\right)\right)^{2}'
    assert latex(laguerre(n, x)) == r'L_{n}\left(x\right)'
    assert latex(laguerre(n, x)**2) == r'\left(L_{n}\left(x\right)\right)^{2}'
    assert latex(assoc_laguerre(n, a, x)) == \
        r'L_{n}^{\left(a\right)}\left(x\right)'
    assert latex(assoc_laguerre(n, a, x)**2) == \
        r'\left(L_{n}^{\left(a\right)}\left(x\right)\right)^{2}'
    assert latex(hermite(n, x)) == r'H_{n}\left(x\right)'
    assert latex(hermite(n, x)**2) == r'\left(H_{n}\left(x\right)\right)^{2}'

    theta = Symbol("theta", real=True)
    phi = Symbol("phi", real=True)
    assert latex(Ynm(n, m, theta, phi)) == r'Y_{n}^{m}\left(\theta,\phi\right)'
    assert latex(Ynm(n, m, theta, phi)**3) == \
        r'\left(Y_{n}^{m}\left(\theta,\phi\right)\right)^{3}'
    assert latex(Znm(n, m, theta, phi)) == r'Z_{n}^{m}\left(\theta,\phi\right)'
    assert latex(Znm(n, m, theta, phi)**3) == \
        r'\left(Z_{n}^{m}\left(\theta,\phi\right)\right)^{3}'

    # Test latex printing of function names with "_"
    assert latex(polar_lift(0)) == \
        r"\operatorname{polar\_lift}{\left(0 \right)}"
    assert latex(polar_lift(0)**3) == \
        r"\operatorname{polar\_lift}^{3}{\left(0 \right)}"

    assert latex(totient(n)) == r'\phi\left(n\right)'
    assert latex(totient(n) ** 2) == r'\left(\phi\left(n\right)\right)^{2}'

    assert latex(reduced_totient(n)) == r'\lambda\left(n\right)'
    assert latex(reduced_totient(n) ** 2) == \
        r'\left(\lambda\left(n\right)\right)^{2}'

    assert latex(divisor_sigma(x)) == r"\sigma\left(x\right)"
    assert latex(divisor_sigma(x)**2) == r"\sigma^{2}\left(x\right)"
    assert latex(divisor_sigma(x, y)) == r"\sigma_y\left(x\right)"
    assert latex(divisor_sigma(x, y)**2) == r"\sigma^{2}_y\left(x\right)"

    assert latex(udivisor_sigma(x)) == r"\sigma^*\left(x\right)"
    assert latex(udivisor_sigma(x)**2) == r"\sigma^*^{2}\left(x\right)"
    assert latex(udivisor_sigma(x, y)) == r"\sigma^*_y\left(x\right)"
    assert latex(udivisor_sigma(x, y)**2) == r"\sigma^*^{2}_y\left(x\right)"

    assert latex(primenu(n)) == r'\nu\left(n\right)'
    assert latex(primenu(n) ** 2) == r'\left(\nu\left(n\right)\right)^{2}'

    assert latex(primeomega(n)) == r'\Omega\left(n\right)'
    assert latex(primeomega(n) ** 2) == \
        r'\left(\Omega\left(n\right)\right)^{2}'

    assert latex(LambertW(n)) == r'W\left(n\right)'
    assert latex(LambertW(n, -1)) == r'W_{-1}\left(n\right)'
    assert latex(LambertW(n, k)) == r'W_{k}\left(n\right)'
    assert latex(LambertW(n) * LambertW(n)) == r"W^{2}\left(n\right)"
    assert latex(Pow(LambertW(n), 2)) == r"W^{2}\left(n\right)"
    assert latex(LambertW(n)**k) == r"W^{k}\left(n\right)"
    assert latex(LambertW(n, k)**p) == r"W^{p}_{k}\left(n\right)"

    assert latex(Mod(x, 7)) == r'x \bmod 7'
    assert latex(Mod(x + 1, 7)) == r'\left(x + 1\right) \bmod 7'
    assert latex(Mod(7, x + 1)) == r'7 \bmod \left(x + 1\right)'
    assert latex(Mod(2 * x, 7)) == r'2 x \bmod 7'
    assert latex(Mod(7, 2 * x)) == r'7 \bmod 2 x'
    assert latex(Mod(x, 7) + 1) == r'\left(x \bmod 7\right) + 1'
    assert latex(2 * Mod(x, 7)) == r'2 \left(x \bmod 7\right)'
    assert latex(Mod(7, 2 * x)**n) == r'\left(7 \bmod 2 x\right)^{n}'

    # some unknown function name should get rendered with \operatorname
    fjlkd = Function('fjlkd')
    assert latex(fjlkd(x)) == r'\operatorname{fjlkd}{\left(x \right)}'
    # even when it is referred to without an argument
    assert latex(fjlkd) == r'\operatorname{fjlkd}'

