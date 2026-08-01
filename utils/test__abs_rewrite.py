
def test_Abs_rewrite():
    x = Symbol('x', real=True)
    a = Abs(x).rewrite(Heaviside).expand()
    assert a == x*Heaviside(x) - x*Heaviside(-x)
    for i in [-2, -1, 0, 1, 2]:
        assert a.subs(x, i) == abs(i)
    y = Symbol('y')
    assert Abs(y).rewrite(Heaviside) == Abs(y)

    x, y = Symbol('x', real=True), Symbol('y')
    assert Abs(x).rewrite(Piecewise) == Piecewise((x, x >= 0), (-x, True))
    assert Abs(y).rewrite(Piecewise) == Abs(y)
    assert Abs(y).rewrite(sign) == y/sign(y)

    i = Symbol('i', imaginary=True)
    assert abs(i).rewrite(Piecewise) == Piecewise((I*i, I*i >= 0), (-I*i, True))


    assert Abs(y).rewrite(conjugate) == sqrt(y*conjugate(y))
    assert Abs(i).rewrite(conjugate) == sqrt(-i**2) #  == -I*i

    y = Symbol('y', extended_real=True)
    assert  (Abs(exp(-I*x)-exp(-I*y))**2).rewrite(conjugate) == \
        -exp(I*x)*exp(-I*y) + 2 - exp(-I*x)*exp(I*y)

