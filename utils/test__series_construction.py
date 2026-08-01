
def test_Series_construction():
    tf = TransferFunction(a0*s**3 + a1*s**2 - a2*s, b0*p**4 + b1*p**3 - b2*s*p, s)
    tf2 = TransferFunction(a2*p - s, a2*s + p, s)
    tf3 = TransferFunction(a0*p + p**a1 - s, p, p)
    tf4 = TransferFunction(1, s**2 + 2*zeta*wn*s + wn**2, s)
    inp = Function('X_d')(s)
    out = Function('X')(s)

    s0 = Series(tf, tf2)
    assert s0.args == (tf, tf2)
    assert s0.var == s

    s1 = Series(Parallel(tf, -tf2), tf2)
    assert s1.args == (Parallel(tf, -tf2), tf2)
    assert s1.var == s

    tf3_ = TransferFunction(inp, 1, s)
    tf4_ = TransferFunction(-out, 1, s)
    s2 = Series(tf, Parallel(tf3_, tf4_), tf2)
    assert s2.args == (tf, Parallel(tf3_, tf4_), tf2)

    s3 = Series(tf, tf2, tf4)
    assert s3.args == (tf, tf2, tf4)

    s4 = Series(tf3_, tf4_)
    assert s4.args == (tf3_, tf4_)
    assert s4.var == s

    s6 = Series(tf2, tf4, Parallel(tf2, -tf), tf4)
    assert s6.args == (tf2, tf4, Parallel(tf2, -tf), tf4)

    s7 = Series(tf, tf2)
    assert s0 == s7
    assert not s0 == s2

    raises(ValueError, lambda: Series(tf, tf3))
    raises(ValueError, lambda: Series(tf, tf2, tf3, tf4))
    raises(ValueError, lambda: Series(-tf3, tf2))
    raises(TypeError, lambda: Series(2, tf, tf4))
    raises(TypeError, lambda: Series(s**2 + p*s, tf3, tf2))
    raises(TypeError, lambda: Series(tf3, Matrix([1, 2, 3, 4])))

