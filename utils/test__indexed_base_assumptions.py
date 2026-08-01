
def test_IndexedBase_assumptions():
    i = Symbol('i', integer=True)
    a = Symbol('a')
    A = IndexedBase(a, positive=True)
    for c in (A, A[i]):
        assert c.is_real
        assert c.is_complex
        assert not c.is_imaginary
        assert c.is_nonnegative
        assert c.is_nonzero
        assert c.is_commutative
        assert log(exp(c)) == c

    assert A != IndexedBase(a)
    assert A == IndexedBase(a, positive=True, real=True)
    assert A[i] != Indexed(a, i)

