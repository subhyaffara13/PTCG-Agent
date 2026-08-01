
def test_U9():
    # Wester sample case for Maple:
    # O29 := diff(f(x, y), x) + diff(f(x, y), y);
    #                      /d         \   /d         \
    #                      |-- f(x, y)| + |-- f(x, y)|
    #                      \dx        /   \dy        /
    #
    # O30 := factor(subs(f(x, y) = g(x^2 + y^2), %));
    #                                2    2
    #                        2 D(g)(x  + y ) (x + y)
    x, y = symbols('x y', real=True)
    su = diff(f(x, y), x) + diff(f(x, y), y)
    s2 = su.subs(f(x, y), g(x**2 + y**2))
    s3 = s2.doit().factor()
    # Subs not performed, s3 = 2*(x + y)*Subs(Derivative(
    #   g(_xi_1), _xi_1), _xi_1, x**2 + y**2)
    # Derivative(g(x*2 + y**2), x**2 + y**2) is not valid in SymPy,
    # and probably will remain that way. You can take derivatives with respect
    # to other expressions only if they are atomic, like a symbol or a
    # function.
    # D operator should be added to SymPy
    # See https://github.com/sympy/sympy/issues/4719.
    assert s3 == (x + y)*Subs(Derivative(g(x), x), x, x**2 + y**2)*2

