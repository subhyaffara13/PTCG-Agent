
def test_epsilon():
    Lorentz = TensorIndexType('Lorentz', dim=4, dummy_name='L')
    a, b, c, d, e = tensor_indices('a,b,c,d,e', Lorentz)
    epsilon = Lorentz.epsilon
    p, q, r, s = tensor_heads('p,q,r,s', [Lorentz])

    t = epsilon(b,a,c,d)
    t1 = t.canon_bp()
    assert t1 == -epsilon(a,b,c,d)

    t = epsilon(c,b,d,a)
    t1 = t.canon_bp()
    assert t1 == epsilon(a,b,c,d)

    t = epsilon(c,a,d,b)
    t1 = t.canon_bp()
    assert t1 == -epsilon(a,b,c,d)

    t = epsilon(a,b,c,d)*p(-a)*q(-b)
    t1 = t.canon_bp()
    assert t1 == epsilon(c,d,a,b)*p(-a)*q(-b)

    t = epsilon(c,b,d,a)*p(-a)*q(-b)
    t1 = t.canon_bp()
    assert t1 == epsilon(c,d,a,b)*p(-a)*q(-b)

    t = epsilon(c,a,d,b)*p(-a)*q(-b)
    t1 = t.canon_bp()
    assert t1 == -epsilon(c,d,a,b)*p(-a)*q(-b)

    t = epsilon(c,a,d,b)*p(-a)*p(-b)
    t1 = t.canon_bp()
    assert t1 == 0

    t = epsilon(c,a,d,b)*p(-a)*q(-b) + epsilon(a,b,c,d)*p(-b)*q(-a)
    t1 = t.canon_bp()
    assert t1 == -2*epsilon(c,d,a,b)*p(-a)*q(-b)

    # Test that epsilon can be create with a SymPy integer:
    Lorentz = TensorIndexType('Lorentz', dim=Integer(4), dummy_name='L')
    epsilon = Lorentz.epsilon
    assert isinstance(epsilon, TensorHead)

