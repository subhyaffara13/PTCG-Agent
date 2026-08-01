
def test_latex_basic():
    assert latex(1 + x) == r"x + 1"
    assert latex(x**2) == r"x^{2}"
    assert latex(x**(1 + x)) == r"x^{x + 1}"
    assert latex(x**3 + x + 1 + x**2) == r"x^{3} + x^{2} + x + 1"

    assert latex(2*x*y) == r"2 x y"
    assert latex(2*x*y, mul_symbol='dot') == r"2 \cdot x \cdot y"
    assert latex(3*x**2*y, mul_symbol='\\,') == r"3\,x^{2}\,y"
    assert latex(1.5*3**x, mul_symbol='\\,') == r"1.5 \cdot 3^{x}"

    assert latex(x**S.Half**5) == r"\sqrt[32]{x}"
    assert latex(Mul(S.Half, x**2, -5, evaluate=False)) == r"\frac{1}{2} x^{2} \left(-5\right)"
    assert latex(Mul(S.Half, x**2, 5, evaluate=False)) == r"\frac{1}{2} x^{2} \cdot 5"
    assert latex(Mul(-5, -5, evaluate=False)) == r"\left(-5\right) \left(-5\right)"
    assert latex(Mul(5, -5, evaluate=False)) == r"5 \left(-5\right)"
    assert latex(Mul(S.Half, -5, S.Half, evaluate=False)) == r"\frac{1}{2} \left(-5\right) \frac{1}{2}"
    assert latex(Mul(5, I, 5, evaluate=False)) == r"5 i 5"
    assert latex(Mul(5, I, -5, evaluate=False)) == r"5 i \left(-5\right)"
    assert latex(Mul(Pow(x, 2), S.Half*x + 1)) == r"x^{2} \left(\frac{x}{2} + 1\right)"
    assert latex(Mul(Pow(x, 3), Rational(2, 3)*x + 1)) == r"x^{3} \left(\frac{2 x}{3} + 1\right)"
    assert latex(Mul(Pow(x, 11), 2*x + 1)) == r"x^{11} \left(2 x + 1\right)"

    assert latex(Mul(0, 1, evaluate=False)) == r'0 \cdot 1'
    assert latex(Mul(1, 0, evaluate=False)) == r'1 \cdot 0'
    assert latex(Mul(1, 1, evaluate=False)) == r'1 \cdot 1'
    assert latex(Mul(-1, 1, evaluate=False)) == r'\left(-1\right) 1'
    assert latex(Mul(1, 1, 1, evaluate=False)) == r'1 \cdot 1 \cdot 1'
    assert latex(Mul(1, 2, evaluate=False)) == r'1 \cdot 2'
    assert latex(Mul(1, S.Half, evaluate=False)) == r'1 \cdot \frac{1}{2}'
    assert latex(Mul(1, 1, S.Half, evaluate=False)) == \
        r'1 \cdot 1 \cdot \frac{1}{2}'
    assert latex(Mul(1, 1, 2, 3, x, evaluate=False)) == \
        r'1 \cdot 1 \cdot 2 \cdot 3 x'
    assert latex(Mul(1, -1, evaluate=False)) == r'1 \left(-1\right)'
    assert latex(Mul(4, 3, 2, 1, 0, y, x, evaluate=False)) == \
        r'4 \cdot 3 \cdot 2 \cdot 1 \cdot 0 y x'
    assert latex(Mul(4, 3, 2, 1+z, 0, y, x, evaluate=False)) == \
        r'4 \cdot 3 \cdot 2 \left(z + 1\right) 0 y x'
    assert latex(Mul(Rational(2, 3), Rational(5, 7), evaluate=False)) == \
        r'\frac{2}{3} \cdot \frac{5}{7}'

    assert latex(1/x) == r"\frac{1}{x}"
    assert latex(1/x, fold_short_frac=True) == r"1 / x"
    assert latex(-S(3)/2) == r"- \frac{3}{2}"
    assert latex(-S(3)/2, fold_short_frac=True) == r"- 3 / 2"
    assert latex(1/x**2) == r"\frac{1}{x^{2}}"
    assert latex(1/(x + y)/2) == r"\frac{1}{2 \left(x + y\right)}"
    assert latex(x/2) == r"\frac{x}{2}"
    assert latex(x/2, fold_short_frac=True) == r"x / 2"
    assert latex((x + y)/(2*x)) == r"\frac{x + y}{2 x}"
    assert latex((x + y)/(2*x), fold_short_frac=True) == \
        r"\left(x + y\right) / 2 x"
    assert latex((x + y)/(2*x), long_frac_ratio=0) == \
        r"\frac{1}{2 x} \left(x + y\right)"
    assert latex((x + y)/x) == r"\frac{x + y}{x}"
    assert latex((x + y)/x, long_frac_ratio=3) == r"\frac{x + y}{x}"
    assert latex((2*sqrt(2)*x)/3) == r"\frac{2 \sqrt{2} x}{3}"
    assert latex((2*sqrt(2)*x)/3, long_frac_ratio=2) == \
        r"\frac{2 x}{3} \sqrt{2}"
    assert latex(binomial(x, y)) == r"{\binom{x}{y}}"

    x_star = Symbol('x^*')
    f = Function('f')
    assert latex(x_star**2) == r"\left(x^{*}\right)^{2}"
    assert latex(x_star**2, parenthesize_super=False) == r"{x^{*}}^{2}"
    assert latex(Derivative(f(x_star), x_star,2)) == r"\frac{d^{2}}{d \left(x^{*}\right)^{2}} f{\left(x^{*} \right)}"
    assert latex(Derivative(f(x_star), x_star,2), parenthesize_super=False) == r"\frac{d^{2}}{d {x^{*}}^{2}} f{\left(x^{*} \right)}"

    assert latex(2*Integral(x, x)/3) == r"\frac{2 \int x\, dx}{3}"
    assert latex(2*Integral(x, x)/3, fold_short_frac=True) == \
        r"\left(2 \int x\, dx\right) / 3"

    assert latex(sqrt(x)) == r"\sqrt{x}"
    assert latex(x**Rational(1, 3)) == r"\sqrt[3]{x}"
    assert latex(x**Rational(1, 3), root_notation=False) == r"x^{\frac{1}{3}}"
    assert latex(sqrt(x)**3) == r"x^{\frac{3}{2}}"
    assert latex(sqrt(x), itex=True) == r"\sqrt{x}"
    assert latex(x**Rational(1, 3), itex=True) == r"\root{3}{x}"
    assert latex(sqrt(x)**3, itex=True) == r"x^{\frac{3}{2}}"
    assert latex(x**Rational(3, 4)) == r"x^{\frac{3}{4}}"
    assert latex(x**Rational(3, 4), fold_frac_powers=True) == r"x^{3/4}"
    assert latex((x + 1)**Rational(3, 4)) == \
        r"\left(x + 1\right)^{\frac{3}{4}}"
    assert latex((x + 1)**Rational(3, 4), fold_frac_powers=True) == \
        r"\left(x + 1\right)^{3/4}"
    assert latex(AlgebraicNumber(sqrt(2))) == r"\sqrt{2}"
    assert latex(AlgebraicNumber(sqrt(2), [3, -7])) == r"-7 + 3 \sqrt{2}"
    assert latex(AlgebraicNumber(sqrt(2), alias='alpha')) == r"\alpha"
    assert latex(AlgebraicNumber(sqrt(2), [3, -7], alias='alpha')) == \
        r"3 \alpha - 7"
    assert latex(AlgebraicNumber(2**(S(1)/3), [1, 3, -7], alias='beta')) == \
        r"\beta^{2} + 3 \beta - 7"

    k = ZZ.cyclotomic_field(5)
    assert latex(k.ext.field_element([1, 2, 3, 4])) == \
        r"\zeta^{3} + 2 \zeta^{2} + 3 \zeta + 4"
    assert latex(k.ext.field_element([1, 2, 3, 4]), order='old') == \
        r"4 + 3 \zeta + 2 \zeta^{2} + \zeta^{3}"
    assert latex(k.primes_above(19)[0]) == \
        r"\left(19, \zeta^{2} + 5 \zeta + 1\right)"
    assert latex(k.primes_above(19)[0], order='old') == \
           r"\left(19, 1 + 5 \zeta + \zeta^{2}\right)"
    assert latex(k.primes_above(7)[0]) == r"\left(7\right)"

    assert latex(1.5e20*x) == r"1.5 \cdot 10^{20} x"
    assert latex(1.5e20*x, mul_symbol='dot') == r"1.5 \cdot 10^{20} \cdot x"
    assert latex(1.5e20*x, mul_symbol='times') == \
        r"1.5 \times 10^{20} \times x"

    assert latex(1/sin(x)) == r"\frac{1}{\sin{\left(x \right)}}"
    assert latex(sin(x)**-1) == r"\frac{1}{\sin{\left(x \right)}}"
    assert latex(sin(x)**Rational(3, 2)) == \
        r"\sin^{\frac{3}{2}}{\left(x \right)}"
    assert latex(sin(x)**Rational(3, 2), fold_frac_powers=True) == \
        r"\sin^{3/2}{\left(x \right)}"

    assert latex(~x) == r"\neg x"
    assert latex(x & y) == r"x \wedge y"
    assert latex(x & y & z) == r"x \wedge y \wedge z"
    assert latex(x | y) == r"x \vee y"
    assert latex(x | y | z) == r"x \vee y \vee z"
    assert latex((x & y) | z) == r"z \vee \left(x \wedge y\right)"
    assert latex(Implies(x, y)) == r"x \Rightarrow y"
    assert latex(~(x >> ~y)) == r"x \not\Rightarrow \neg y"
    assert latex(Implies(Or(x,y), z)) == r"\left(x \vee y\right) \Rightarrow z"
    assert latex(Implies(z, Or(x,y))) == r"z \Rightarrow \left(x \vee y\right)"
    assert latex(~(x & y)) == r"\neg \left(x \wedge y\right)"

    assert latex(~x, symbol_names={x: "x_i"}) == r"\neg x_i"
    assert latex(x & y, symbol_names={x: "x_i", y: "y_i"}) == \
        r"x_i \wedge y_i"
    assert latex(x & y & z, symbol_names={x: "x_i", y: "y_i", z: "z_i"}) == \
        r"x_i \wedge y_i \wedge z_i"
    assert latex(x | y, symbol_names={x: "x_i", y: "y_i"}) == r"x_i \vee y_i"
    assert latex(x | y | z, symbol_names={x: "x_i", y: "y_i", z: "z_i"}) == \
        r"x_i \vee y_i \vee z_i"
    assert latex((x & y) | z, symbol_names={x: "x_i", y: "y_i", z: "z_i"}) == \
        r"z_i \vee \left(x_i \wedge y_i\right)"
    assert latex(Implies(x, y), symbol_names={x: "x_i", y: "y_i"}) == \
        r"x_i \Rightarrow y_i"
    assert latex(Pow(Rational(1, 3), -1, evaluate=False)) == r"\frac{1}{\frac{1}{3}}"
    assert latex(Pow(Rational(1, 3), -2, evaluate=False)) == r"\frac{1}{(\frac{1}{3})^{2}}"
    assert latex(Pow(Integer(1)/100, -1, evaluate=False)) == r"\frac{1}{\frac{1}{100}}"

    p = Symbol('p', positive=True)
    assert latex(exp(-p)*log(p)) == r"e^{- p} \log{\left(p \right)}"

    assert latex(Pow(Rational(2, 3), -1, evaluate=False)) == r'\frac{1}{\frac{2}{3}}'
    assert latex(Pow(Rational(4, 3), -1, evaluate=False)) == r'\frac{1}{\frac{4}{3}}'
    assert latex(Pow(Rational(-3, 4), -1, evaluate=False)) == r'\frac{1}{- \frac{3}{4}}'
    assert latex(Pow(Rational(-4, 4), -1, evaluate=False)) == r'\frac{1}{-1}'
    assert latex(Pow(Rational(1, 3), -1, evaluate=False)) == r'\frac{1}{\frac{1}{3}}'
    assert latex(Pow(Rational(-1, 3), -1, evaluate=False)) == r'\frac{1}{- \frac{1}{3}}'

