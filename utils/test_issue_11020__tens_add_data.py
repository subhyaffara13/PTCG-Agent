
def test_issue_11020_TensAdd_data():
    with warns_deprecated_sympy():
        Lorentz = TensorIndexType('Lorentz', metric_symmetry=1, dummy_name='i', dim=2)
        Lorentz.data = [-1, 1]

        a, b, c, d = tensor_indices('a, b, c, d', Lorentz)
        i0, i1 = tensor_indices('i_0:2', Lorentz)

        # metric tensor
        g = TensorHead('g', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
        g.data = Lorentz.data

        u = TensorHead('u', [Lorentz])
        u.data = [1, 0]

        add_1 = g(b, c) * g(d, i0) * u(-i0) - g(b, c) * u(d)
        assert (add_1.data == Array.zeros(2, 2, 2))
        # Now let us replace index `d` with `a`:
        add_2 = g(b, c) * g(a, i0) * u(-i0) - g(b, c) * u(a)
        assert (add_2.data == Array.zeros(2, 2, 2))

        # some more tests
        # perp is tensor orthogonal to u^\mu
        perp = u(a) * u(b) + g(a, b)
        mul_1 = u(-a) * perp(a, b)
        assert (mul_1.data == Array([0, 0]))

        mul_2 = u(-c) * perp(c, a) * perp(d, b)
        assert (mul_2.data == Array.zeros(2, 2, 2))

