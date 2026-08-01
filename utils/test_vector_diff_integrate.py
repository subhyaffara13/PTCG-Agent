
def test_vector_diff_integrate():
    f = Function('f')
    v = f(a)*C.i + a**2*C.j - C.k
    assert Derivative(v, a) == Derivative((f(a))*C.i +
                                          a**2*C.j + (-1)*C.k, a)
    assert (diff(v, a) == v.diff(a) == Derivative(v, a).doit() ==
            (Derivative(f(a), a))*C.i + 2*a*C.j)
    assert (Integral(v, a) == (Integral(f(a), a))*C.i +
            (Integral(a**2, a))*C.j + (Integral(-1, a))*C.k)

