
def test_latex_derivatives():
    # regular "d" for ordinary derivatives
    assert latex(diff(x**3, x, evaluate=False)) == \
        r"\frac{d}{d x} x^{3}"
    assert latex(diff(sin(x) + x**2, x, evaluate=False)) == \
        r"\frac{d}{d x} \left(x^{2} + \sin{\left(x \right)}\right)"
    assert latex(diff(diff(sin(x) + x**2, x, evaluate=False), evaluate=False))\
        == \
        r"\frac{d^{2}}{d x^{2}} \left(x^{2} + \sin{\left(x \right)}\right)"
    assert latex(diff(diff(diff(sin(x) + x**2, x, evaluate=False), evaluate=False), evaluate=False)) == \
        r"\frac{d^{3}}{d x^{3}} \left(x^{2} + \sin{\left(x \right)}\right)"

    # \partial for partial derivatives
    assert latex(diff(sin(x * y), x, evaluate=False)) == \
        r"\frac{\partial}{\partial x} \sin{\left(x y \right)}"
    assert latex(diff(sin(x * y) + x**2, x, evaluate=False)) == \
        r"\frac{\partial}{\partial x} \left(x^{2} + \sin{\left(x y \right)}\right)"
    assert latex(diff(diff(sin(x*y) + x**2, x, evaluate=False), x, evaluate=False)) == \
        r"\frac{\partial^{2}}{\partial x^{2}} \left(x^{2} + \sin{\left(x y \right)}\right)"
    assert latex(diff(diff(diff(sin(x*y) + x**2, x, evaluate=False), x, evaluate=False), x, evaluate=False)) == \
        r"\frac{\partial^{3}}{\partial x^{3}} \left(x^{2} + \sin{\left(x y \right)}\right)"

    # mixed partial derivatives
    f = Function("f")
    assert latex(diff(diff(f(x, y), x, evaluate=False), y, evaluate=False)) == \
        r"\frac{\partial^{2}}{\partial y\partial x} " + latex(f(x, y))

    assert latex(diff(diff(diff(f(x, y), x, evaluate=False), x, evaluate=False), y, evaluate=False)) == \
        r"\frac{\partial^{3}}{\partial y\partial x^{2}} " + latex(f(x, y))

    # for negative nested Derivative
    assert latex(diff(-diff(y**2,x,evaluate=False),x,evaluate=False)) == r'\frac{d}{d x} \left(- \frac{d}{d x} y^{2}\right)'
    assert latex(diff(diff(-diff(diff(y,x,evaluate=False),x,evaluate=False),x,evaluate=False),x,evaluate=False)) == \
        r'\frac{d^{2}}{d x^{2}} \left(- \frac{d^{2}}{d x^{2}} y\right)'

    # use ordinary d when one of the variables has been integrated out
    assert latex(diff(Integral(exp(-x*y), (x, 0, oo)), y, evaluate=False)) == \
        r"\frac{d}{d y} \int\limits_{0}^{\infty} e^{- x y}\, dx"

    # Derivative wrapped in power:
    assert latex(diff(x, x, evaluate=False)**2) == \
        r"\left(\frac{d}{d x} x\right)^{2}"

    assert latex(diff(f(x), x)**2) == \
        r"\left(\frac{d}{d x} f{\left(x \right)}\right)^{2}"

    assert latex(diff(f(x), (x, n))) == \
        r"\frac{d^{n}}{d x^{n}} f{\left(x \right)}"

    x1 = Symbol('x1')
    x2 = Symbol('x2')
    assert latex(diff(f(x1, x2), x1)) == r'\frac{\partial}{\partial x_{1}} f{\left(x_{1},x_{2} \right)}'

    n1 = Symbol('n1')
    assert latex(diff(f(x), (x, n1))) == r'\frac{d^{n_{1}}}{d x^{n_{1}}} f{\left(x \right)}'

    n2 = Symbol('n2')
    assert latex(diff(f(x), (x, Max(n1, n2)))) == \
        r'\frac{d^{\max\left(n_{1}, n_{2}\right)}}{d x^{\max\left(n_{1}, n_{2}\right)}} f{\left(x \right)}'

    # set diff operator
    assert latex(diff(f(x), x), diff_operator="rd") == r'\frac{\mathrm{d}}{\mathrm{d} x} f{\left(x \right)}'

