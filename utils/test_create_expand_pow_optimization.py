
def test_create_expand_pow_optimization():
    cc = lambda x: ccode(
        optimize(x, [create_expand_pow_optimization(4)]))
    x = Symbol('x')
    assert cc(x**4) == 'x*x*x*x'
    assert cc(x**4 + x**2) == 'x*x + x*x*x*x'
    assert cc(x**5 + x**4) == 'pow(x, 5) + x*x*x*x'
    assert cc(sin(x)**4) == 'pow(sin(x), 4)'
    # gh issue 15335
    assert cc(x**(-4)) == '1.0/(x*x*x*x)'
    assert cc(x**(-5)) == 'pow(x, -5)'
    assert cc(-x**4) == '-(x*x*x*x)'
    assert cc(x**4 - x**2) == '-(x*x) + x*x*x*x'
    i = Symbol('i', integer=True)
    assert cc(x**i - x**2) == 'pow(x, i) - (x*x)'
    y = Symbol('y', real=True)
    assert cc(Abs(exp(y**4))) == "exp(y*y*y*y)"

    # gh issue 20753
    cc2 = lambda x: ccode(optimize(x, [create_expand_pow_optimization(
        4, base_req=lambda b: b.is_Function)]))
    assert cc2(x**3 + sin(x)**3) == "pow(x, 3) + sin(x)*sin(x)*sin(x)"

