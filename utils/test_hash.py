
def test_hash():
    class Hashable:
        def __init__(self, value):
            self.value = value

        def __hash__(self):
            return self.value

    class Unhashable:
        __hash__ = None

    assert m.hash_function(Hashable(42)) == 42
    with pytest.raises(TypeError):
        m.hash_function(Unhashable())


def test_hash():
    D = Symbol('D')
    Lorentz = TensorIndexType('Lorentz', dim=D, dummy_name='L')
    a, b, c, d, e = tensor_indices('a,b,c,d,e', Lorentz)
    g = Lorentz.metric

    p, q = tensor_heads('p q', [Lorentz])
    p_type = p.args[1]
    t1 = p(a)*q(b)
    t2 = p(a)*p(b)
    assert hash(t1) != hash(t2)
    t3 = p(a)*p(b) + g(a,b)
    t4 = p(a)*p(b) - g(a,b)
    assert hash(t3) != hash(t4)

    assert a.func(*a.args) == a
    assert Lorentz.func(*Lorentz.args) == Lorentz
    assert g.func(*g.args) == g
    assert p.func(*p.args) == p
    assert p_type.func(*p_type.args) == p_type
    assert p(a).func(*(p(a)).args) == p(a)
    assert t1.func(*t1.args) == t1
    assert t2.func(*t2.args) == t2
    assert t3.func(*t3.args) == t3
    assert t4.func(*t4.args) == t4

    assert hash(a.func(*a.args)) == hash(a)
    assert hash(Lorentz.func(*Lorentz.args)) == hash(Lorentz)
    assert hash(g.func(*g.args)) == hash(g)
    assert hash(p.func(*p.args)) == hash(p)
    assert hash(p_type.func(*p_type.args)) == hash(p_type)
    assert hash(p(a).func(*(p(a)).args)) == hash(p(a))
    assert hash(t1.func(*t1.args)) == hash(t1)
    assert hash(t2.func(*t2.args)) == hash(t2)
    assert hash(t3.func(*t3.args)) == hash(t3)
    assert hash(t4.func(*t4.args)) == hash(t4)

    def check_all(obj):
        return all(isinstance(_, Basic) for _ in obj.args)

    assert check_all(a)
    assert check_all(Lorentz)
    assert check_all(g)
    assert check_all(p)
    assert check_all(p_type)
    assert check_all(p(a))
    assert check_all(t1)
    assert check_all(t2)
    assert check_all(t3)
    assert check_all(t4)

    tsymmetry = TensorSymmetry.direct_product(-2, 1, 3)

    assert tsymmetry.func(*tsymmetry.args) == tsymmetry
    assert hash(tsymmetry.func(*tsymmetry.args)) == hash(tsymmetry)
    assert check_all(tsymmetry)


def test_hash():
    for cls in classes[-2:]:
        s = {cls.eye(1), cls.eye(1)}
        assert len(s) == 1 and s.pop() == cls.eye(1)
    # issue 3979
    for cls in classes[:2]:
        assert not isinstance(cls.eye(1), Hashable)


def test_hash():
    for cls in immutable_classes:
        s = {cls.eye(1), cls.eye(1)}
        assert len(s) == 1 and s.pop() == cls.eye(1)
    # issue 3979
    for cls in mutable_classes:
        assert not isinstance(cls.eye(1), Hashable)


def test_hash(thunk):
    assert thunk() in {thunk()}


def test_hash():
    for i in range(-256, 256):
        assert hash(mpf(i)) == hash(i)
    assert hash(mpf(0.5)) == hash(0.5)
    assert hash(mpc(2,3)) == hash(2+3j)
    # Check that this doesn't fail
    assert hash(inf)
    # Check that overflow doesn't assign equal hashes to large numbers
    assert hash(mpf('1e1000')) != hash('1e10000')
    assert hash(mpc(100,'1e1000')) != hash(mpc(200,'1e1000'))
    from mpmath.rational import mpq
    assert hash(mp.mpq(1,3))
    assert hash(mp.mpq(0,1)) == 0
    assert hash(mp.mpq(-1,1)) == hash(-1)
    assert hash(mp.mpq(1,1)) == hash(1)
    assert hash(mp.mpq(5,1)) == hash(5)
    assert hash(mp.mpq(1,2)) == hash(0.5)
    if sys.version_info >= (3, 2):
        assert hash(mpf(1)*2**2000) == hash(2**2000)
        assert hash(mpf(1)/2**2000) == hash(mpq(1,2**2000))

