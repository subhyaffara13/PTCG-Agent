
def test_special_eq_ne():
    # test special equality cases:
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b, d0, d1, i, j, k = tensor_indices('a,b,d0,d1,i,j,k', Lorentz)
    # A, B symmetric
    A, B = tensor_heads('A,B', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    p, q, r = tensor_heads('p,q,r', [Lorentz])

    t = 0*A(a, b)
    assert _is_equal(t, 0)
    assert _is_equal(t, S.Zero)

    assert p(i) != A(a, b)
    assert A(a, -a) != A(a, b)
    assert 0*(A(a, b) + B(a, b)) == 0
    assert 0*(A(a, b) + B(a, b)) is S.Zero

    assert 3*(A(a, b) - A(a, b)) is S.Zero

    assert p(i) + q(i) != A(a, b)
    assert p(i) + q(i) != A(a, b) + B(a, b)

    assert p(i) - p(i) == 0
    assert p(i) - p(i) is S.Zero

    assert _is_equal(A(a, b), A(b, a))

