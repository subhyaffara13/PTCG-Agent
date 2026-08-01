
def test_riemann_cyclic_replace():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    m0, m1, m2, m3 = tensor_indices('m:4', Lorentz)
    R = TensorHead('R', [Lorentz]*4, TensorSymmetry.riemann())
    t = R(m0, m2, m1, m3)
    t1 = riemann_cyclic_replace(t)
    t1a = Rational(-1, 3)*R(m0, m3, m2, m1) + Rational(1, 3)*R(m0, m1, m2, m3) + Rational(2, 3)*R(m0, m2, m1, m3)
    assert t1 == t1a

