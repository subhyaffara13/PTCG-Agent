
def test_powm1():
    args = x, y = map(Symbol, "xy")

    expr1 = x**y - 1
    opt1 = optimize(expr1, [powm1_opt])
    assert opt1 == powm1(x, y)
    for arg in args:
        assert expr1.diff(arg) == opt1.diff(arg)
    if scipy and tuple(map(int, scipy.version.version.split('.')[:3])) >= (1, 10, 0):
        subs1_a = {x: Rational(*(1.0+1e-13).as_integer_ratio()), y: pi}
        ref1_f64_a = 3.139081648208105e-13
        _check_num_lambdify(expr1, opt1, subs1_a, ref1_f64_a, lambdify_kw={"modules": 'scipy'}, poorness=10**11)

        subs1_b = {x: pi, y: Rational(*(1e-10).as_integer_ratio())}
        ref1_f64_b = 1.1447298859149205e-10
        _check_num_lambdify(expr1, opt1, subs1_b, ref1_f64_b, lambdify_kw={"modules": 'scipy'}, poorness=10**9)


def test_powm1():
    cases = {
            powm1(x, y): x**y - 1,
            powm1(x*y, z): (x*y)**z - 1,
            powm1(x, y*z): x**(y*z)-1,
            powm1(x*y*z, x*y*z): (x*y*z)**(x*y*z)-1
    }
    for pm1_e, ref_e in cases.items():
        for wrt, deriv_order in product([x, y, z], range(3)):
            der = pm1_e.diff(wrt, deriv_order)
            ref = ref_e.diff(wrt, deriv_order)
            delta = (der - ref).rewrite(Pow)
            assert delta.simplify() == 0

    eulers_constant_m1 = powm1(x, 1/log(x))
    assert eulers_constant_m1.rewrite(Pow) == exp(1) - 1
    assert eulers_constant_m1.simplify() == exp(1) - 1


def test_powm1(x, y, expected, rtol):
    p = powm1(x, y)
    assert_allclose(p, expected, rtol=rtol)


def test_powm1():
    mp.dps = 15
    assert powm1(2,3) == 7
    assert powm1(-1,2) == 0
    assert powm1(-1,0) == 0
    assert powm1(-2,0) == 0
    assert powm1(3+4j,0) == 0
    assert powm1(0,1) == -1
    assert powm1(0,0) == 0
    assert powm1(1,0) == 0
    assert powm1(1,2) == 0
    assert powm1(1,3+4j) == 0
    assert powm1(1,5) == 0
    assert powm1(j,4) == 0
    assert powm1(-j,4) == 0
    assert (powm1(2,1e-100)*1e100).ae(ln2)
    assert powm1(2,'1e-100000000000') != 0
    assert (powm1(fadd(1,1e-100,exact=True), 5)*1e100).ae(5)

