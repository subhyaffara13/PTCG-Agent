
def test_add2():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    m, n, p, q = tensor_indices('m,n,p,q', Lorentz)
    R = TensorHead('R', [Lorentz]*4, TensorSymmetry.riemann())
    A = TensorHead('A', [Lorentz]*3, TensorSymmetry.fully_symmetric(-3))
    t1 = 2*R(m, n, p, q) - R(m, q, n, p) + R(m, p, n, q)
    t2 = t1*A(-n, -p, -q)
    t2 = t2.canon_bp()
    assert t2 == 0
    t1 = Rational(2, 3)*R(m,n,p,q) - Rational(1, 3)*R(m,q,n,p) + Rational(1, 3)*R(m,p,n,q)
    t2 = t1*A(-n, -p, -q)
    t2 = t2.canon_bp()
    assert t2 == 0
    t = A(m, -m, n) + A(n, p, -p)
    t = t.canon_bp()
    assert t == 0

