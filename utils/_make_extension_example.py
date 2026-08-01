
def _make_extension_example():
    # https://github.com/sympy/sympy/issues/18531
    from sympy.core import Mul
    def mul2(expr):
        # 2-arg mul hack...
        return Mul(2, expr, evaluate=False)

    f = ((x**2 + 1)**3/((x - 1)**2*(x + 1)**2*(-x**2 + 2*x + 1)*(x**2 + 2*x - 1)))
    g = (1/mul2(x - sqrt(2) + 1)
       - 1/mul2(x - sqrt(2) - 1)
       + 1/mul2(x + 1 + sqrt(2))
       - 1/mul2(x - 1 + sqrt(2))
       + 1/mul2((x + 1)**2)
       + 1/mul2((x - 1)**2))
    return f, g

