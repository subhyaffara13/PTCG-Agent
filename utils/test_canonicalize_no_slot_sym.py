
def test_canonicalize_no_slot_sym():
    # A_d0 * B^d0; T_c = A^d0*B_d0
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b, d0, d1 = tensor_indices('a,b,d0,d1', Lorentz)
    A, B = tensor_heads('A,B', [Lorentz], TensorSymmetry.no_symmetry(1))
    t = A(-d0)*B(d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0)*B(-L_0)'

    # A^a * B^b;  T_c = T
    t = A(a)*B(b)
    tc = t.canon_bp()
    assert tc == t
    # B^b * A^a
    t1 = B(b)*A(a)
    tc = t1.canon_bp()
    assert str(tc) == 'A(a)*B(b)'

    # A symmetric
    # A^{b}_{d0}*A^{d0, a}; T_c = A^{a d0}*A{b}_{d0}
    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = A(b, -d0)*A(d0, a)
    tc = t.canon_bp()
    assert str(tc) == 'A(a, L_0)*A(b, -L_0)'

    # A^{d1}_{d0}*B^d0*C_d1
    # T_c = A^{d0 d1}*B_d0*C_d1
    B, C = tensor_heads('B,C', [Lorentz], TensorSymmetry.no_symmetry(1))
    t = A(d1, -d0)*B(d0)*C(-d1)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1)*B(-L_0)*C(-L_1)'

    # A without symmetry
    # A^{d1}_{d0}*B^d0*C_d1 ord=[d0,-d0,d1,-d1]; g = [2,1,0,3,4,5]
    # T_c = A^{d0 d1}*B_d1*C_d0; can = [0,2,3,1,4,5]
    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.no_symmetry(2))
    t = A(d1, -d0)*B(d0)*C(-d1)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1)*B(-L_1)*C(-L_0)'

    # A, B without symmetry
    # A^{d1}_{d0}*B_{d1}^{d0}
    # T_c = A^{d0 d1}*B_{d0 d1}
    B = TensorHead('B', [Lorentz]*2, TensorSymmetry.no_symmetry(2))
    t = A(d1, -d0)*B(-d1, d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1)*B(-L_0, -L_1)'
    # A_{d0}^{d1}*B_{d1}^{d0}
    # T_c = A^{d0 d1}*B_{d1 d0}
    t = A(-d0, d1)*B(-d1, d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1)*B(-L_1, -L_0)'

    # A, B, C without symmetry
    # A^{d1 d0}*B_{a d0}*C_{d1 b}
    # T_c=A^{d0 d1}*B_{a d1}*C_{d0 b}
    C = TensorHead('C', [Lorentz]*2, TensorSymmetry.no_symmetry(2))
    t = A(d1, d0)*B(-a, -d0)*C(-d1, -b)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1)*B(-a, -L_1)*C(-L_0, -b)'

    # A symmetric, B and C without symmetry
    # A^{d1 d0}*B_{a d0}*C_{d1 b}
    # T_c = A^{d0 d1}*B_{a d0}*C_{d1 b}
    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = A(d1, d0)*B(-a, -d0)*C(-d1, -b)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1)*B(-a, -L_0)*C(-L_1, -b)'

    # A and C symmetric, B without symmetry
    # A^{d1 d0}*B_{a d0}*C_{d1 b} ord=[a,b,d0,-d0,d1,-d1]
    # T_c = A^{d0 d1}*B_{a d0}*C_{b d1}
    C = TensorHead('C', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = A(d1, d0)*B(-a, -d0)*C(-d1, -b)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1)*B(-a, -L_0)*C(-b, -L_1)'


def test_canonicalize_no_slot_sym():
    # cases in which there is no slot symmetry after fixing the
    # free indices; here and in the following if the symmetry of the
    # metric is not specified, it is assumed to be symmetric.
    # If it is not specified, tensors are commuting.

    # A_d0 * B^d0; g = [1,0, 2,3]; T_c = A^d0*B_d0; can = [0,1,2,3]
    base1, gens1 = get_symmetric_group_sgs(1)
    dummies = [0, 1]
    g = Permutation([1,0,2,3])
    can = canonicalize(g, dummies, 0, (base1,gens1,1,0), (base1,gens1,1,0))
    assert can == [0,1,2,3]
    # equivalently
    can = canonicalize(g, dummies, 0, (base1, gens1, 2, None))
    assert can == [0,1,2,3]

    # with antisymmetric metric; T_c = -A^d0*B_d0; can = [0,1,3,2]
    can = canonicalize(g, dummies, 1, (base1,gens1,1,0), (base1,gens1,1,0))
    assert can == [0,1,3,2]

    # A^a * B^b; ord = [a,b]; g = [0,1,2,3]; can = g
    g = Permutation([0,1,2,3])
    dummies = []
    t0 = t1 = (base1, gens1, 1, 0)
    can = canonicalize(g, dummies, 0, t0, t1)
    assert can == [0,1,2,3]
    # B^b * A^a
    g = Permutation([1,0,2,3])
    can = canonicalize(g, dummies, 0, t0, t1)
    assert can == [1,0,2,3]

    # A symmetric
    # A^{b}_{d0}*A^{d0, a} order a,b,d0,-d0; T_c = A^{a d0}*A{b}_{d0}
    # g = [1,3,2,0,4,5]; can = [0,2,1,3,4,5]
    base2, gens2 = get_symmetric_group_sgs(2)
    dummies = [2,3]
    g = Permutation([1,3,2,0,4,5])
    can = canonicalize(g, dummies, 0, (base2, gens2, 2, 0))
    assert can == [0, 2, 1, 3, 4, 5]
    # with antisymmetric metric
    can = canonicalize(g, dummies, 1, (base2, gens2, 2, 0))
    assert can == [0, 2, 1, 3, 4, 5]
    # A^{a}_{d0}*A^{d0, b}
    g = Permutation([0,3,2,1,4,5])
    can = canonicalize(g, dummies, 1, (base2, gens2, 2, 0))
    assert can == [0, 2, 1, 3, 5, 4]

    # A, B symmetric
    # A^b_d0*B^{d0,a}; g=[1,3,2,0,4,5]
    # T_c = A^{b,d0}*B_{a,d0}; can = [1,2,0,3,4,5]
    dummies = [2,3]
    g = Permutation([1,3,2,0,4,5])
    can = canonicalize(g, dummies, 0, (base2,gens2,1,0), (base2,gens2,1,0))
    assert can == [1,2,0,3,4,5]
    # same with antisymmetric metric
    can = canonicalize(g, dummies, 1, (base2,gens2,1,0), (base2,gens2,1,0))
    assert can == [1,2,0,3,5,4]

    # A^{d1}_{d0}*B^d0*C_d1 ord=[d0,-d0,d1,-d1]; g = [2,1,0,3,4,5]
    # T_c = A^{d0 d1}*B_d0*C_d1; can = [0,2,1,3,4,5]
    base1, gens1 = get_symmetric_group_sgs(1)
    base2, gens2 = get_symmetric_group_sgs(2)
    g = Permutation([2,1,0,3,4,5])
    dummies = [0,1,2,3]
    t0 = (base2, gens2, 1, 0)
    t1 = t2 = (base1, gens1, 1, 0)
    can = canonicalize(g, dummies, 0, t0, t1, t2)
    assert can == [0, 2, 1, 3, 4, 5]

    # A without symmetry
    # A^{d1}_{d0}*B^d0*C_d1 ord=[d0,-d0,d1,-d1]; g = [2,1,0,3,4,5]
    # T_c = A^{d0 d1}*B_d1*C_d0; can = [0,2,3,1,4,5]
    g = Permutation([2,1,0,3,4,5])
    dummies = [0,1,2,3]
    t0 = ([], [Permutation(list(range(4)))], 1, 0)
    can = canonicalize(g, dummies, 0, t0, t1, t2)
    assert can == [0,2,3,1,4,5]
    # A, B without symmetry
    # A^{d1}_{d0}*B_{d1}^{d0}; g = [2,1,3,0,4,5]
    # T_c = A^{d0 d1}*B_{d0 d1}; can = [0,2,1,3,4,5]
    t0 = t1 = ([], [Permutation(list(range(4)))], 1, 0)
    dummies = [0,1,2,3]
    g = Permutation([2,1,3,0,4,5])
    can = canonicalize(g, dummies, 0, t0, t1)
    assert can == [0, 2, 1, 3, 4, 5]
    # A_{d0}^{d1}*B_{d1}^{d0}; g = [1,2,3,0,4,5]
    # T_c = A^{d0 d1}*B_{d1 d0}; can = [0,2,3,1,4,5]
    g = Permutation([1,2,3,0,4,5])
    can = canonicalize(g, dummies, 0, t0, t1)
    assert can == [0,2,3,1,4,5]

    # A, B, C without symmetry
    # A^{d1 d0}*B_{a d0}*C_{d1 b} ord=[a,b,d0,-d0,d1,-d1]
    # g=[4,2,0,3,5,1,6,7]
    # T_c=A^{d0 d1}*B_{a d1}*C_{d0 b}; can = [2,4,0,5,3,1,6,7]
    t0 = t1 = t2 = ([], [Permutation(list(range(4)))], 1, 0)
    dummies = [2,3,4,5]
    g = Permutation([4,2,0,3,5,1,6,7])
    can = canonicalize(g, dummies, 0, t0, t1, t2)
    assert can == [2,4,0,5,3,1,6,7]

    # A symmetric, B and C without symmetry
    # A^{d1 d0}*B_{a d0}*C_{d1 b} ord=[a,b,d0,-d0,d1,-d1]
    # g=[4,2,0,3,5,1,6,7]
    # T_c = A^{d0 d1}*B_{a d0}*C_{d1 b}; can = [2,4,0,3,5,1,6,7]
    t0 = (base2,gens2,1,0)
    t1 = t2 = ([], [Permutation(list(range(4)))], 1, 0)
    dummies = [2,3,4,5]
    g = Permutation([4,2,0,3,5,1,6,7])
    can = canonicalize(g, dummies, 0, t0, t1, t2)
    assert can == [2,4,0,3,5,1,6,7]

    # A and C symmetric, B without symmetry
    # A^{d1 d0}*B_{a d0}*C_{d1 b} ord=[a,b,d0,-d0,d1,-d1]
    # g=[4,2,0,3,5,1,6,7]
    # T_c = A^{d0 d1}*B_{a d0}*C_{b d1}; can = [2,4,0,3,1,5,6,7]
    t0 = t2 = (base2,gens2,1,0)
    t1 = ([], [Permutation(list(range(4)))], 1, 0)
    dummies = [2,3,4,5]
    g = Permutation([4,2,0,3,5,1,6,7])
    can = canonicalize(g, dummies, 0, t0, t1, t2)
    assert can == [2,4,0,3,1,5,6,7]

    # A symmetric, B without symmetry, C antisymmetric
    # A^{d1 d0}*B_{a d0}*C_{d1 b} ord=[a,b,d0,-d0,d1,-d1]
    # g=[4,2,0,3,5,1,6,7]
    # T_c = -A^{d0 d1}*B_{a d0}*C_{b d1}; can = [2,4,0,3,1,5,7,6]
    t0 = (base2,gens2, 1, 0)
    t1 = ([], [Permutation(list(range(4)))], 1, 0)
    base2a, gens2a = get_symmetric_group_sgs(2, 1)
    t2 = (base2a, gens2a, 1, 0)
    dummies = [2,3,4,5]
    g = Permutation([4,2,0,3,5,1,6,7])
    can = canonicalize(g, dummies, 0, t0, t1, t2)
    assert can == [2,4,0,3,1,5,7,6]

