
def test_canonicalize_no_dummies():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b, c, d = tensor_indices('a, b, c, d', Lorentz)

    # A commuting
    # A^c A^b A^a
    # T_c = A^a A^b A^c
    A = TensorHead('A', [Lorentz], TensorSymmetry.no_symmetry(1))
    t = A(c)*A(b)*A(a)
    tc = t.canon_bp()
    assert str(tc) == 'A(a)*A(b)*A(c)'

    # A anticommuting
    # A^c A^b A^a
    # T_c = -A^a A^b A^c
    A = TensorHead('A', [Lorentz], TensorSymmetry.no_symmetry(1), 1)
    t = A(c)*A(b)*A(a)
    tc = t.canon_bp()
    assert str(tc) == '-A(a)*A(b)*A(c)'

    # A commuting and symmetric
    # A^{b,d}*A^{c,a}
    # T_c = A^{a c}*A^{b d}
    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = A(b, d)*A(c, a)
    tc = t.canon_bp()
    assert str(tc) == 'A(a, c)*A(b, d)'

    # A anticommuting and symmetric
    # A^{b,d}*A^{c,a}
    # T_c = -A^{a c}*A^{b d}
    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.fully_symmetric(2), 1)
    t = A(b, d)*A(c, a)
    tc = t.canon_bp()
    assert str(tc) == '-A(a, c)*A(b, d)'

    # A^{c,a}*A^{b,d}
    # T_c = A^{a c}*A^{b d}
    t = A(c, a)*A(b, d)
    tc = t.canon_bp()
    assert str(tc) == 'A(a, c)*A(b, d)'


def test_canonicalize_no_dummies():
    base1, gens1 = get_symmetric_group_sgs(1)
    base2, gens2 = get_symmetric_group_sgs(2)
    base2a, gens2a = get_symmetric_group_sgs(2, 1)

    # A commuting
    # A^c A^b A^a; ord = [a,b,c]; g = [2,1,0,3,4]
    # T_c = A^a A^b A^c; can = list(range(5))
    g = Permutation([2,1,0,3,4])
    can = canonicalize(g, [], 0, (base1, gens1, 3, 0))
    assert can == list(range(5))

    # A anticommuting
    # A^c A^b A^a; ord = [a,b,c]; g = [2,1,0,3,4]
    # T_c = -A^a A^b A^c; can = [0,1,2,4,3]
    g = Permutation([2,1,0,3,4])
    can = canonicalize(g, [], 0, (base1, gens1, 3, 1))
    assert can == [0,1,2,4,3]

    # A commuting and symmetric
    # A^{b,d}*A^{c,a}; ord = [a,b,c,d]; g = [1,3,2,0,4,5]
    # T_c = A^{a c}*A^{b d}; can = [0,2,1,3,4,5]
    g = Permutation([1,3,2,0,4,5])
    can = canonicalize(g, [], 0, (base2, gens2, 2, 0))
    assert can == [0,2,1,3,4,5]

    # A anticommuting and symmetric
    # A^{b,d}*A^{c,a}; ord = [a,b,c,d]; g = [1,3,2,0,4,5]
    # T_c = -A^{a c}*A^{b d}; can = [0,2,1,3,5,4]
    g = Permutation([1,3,2,0,4,5])
    can = canonicalize(g, [], 0, (base2, gens2, 2, 1))
    assert can == [0,2,1,3,5,4]
    # A^{c,a}*A^{b,d} ; g = [2,0,1,3,4,5]
    # T_c = A^{a c}*A^{b d}; can = [0,2,1,3,4,5]
    g = Permutation([2,0,1,3,4,5])
    can = canonicalize(g, [], 0, (base2, gens2, 2, 1))
    assert can == [0,2,1,3,4,5]

