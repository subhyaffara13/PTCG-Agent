
def test_pdsolve_all():
    f, F = map(Function, ['f', 'F'])
    u = f(x,y)
    eq = u + u.diff(x) + u.diff(y) + x**2*y
    sol = pdsolve(eq, hint = 'all')
    keys = ['1st_linear_constant_coeff',
        '1st_linear_constant_coeff_Integral', 'default', 'order']
    assert sorted(sol.keys()) == keys
    assert sol['order'] == 1
    assert sol['default'] == '1st_linear_constant_coeff'
    assert sol['1st_linear_constant_coeff'].expand() == Eq(f(x, y),
        -x**2*y + x**2 + 2*x*y - 4*x - 2*y + F(x - y)*exp(-x/2 - y/2) + 6).expand()

