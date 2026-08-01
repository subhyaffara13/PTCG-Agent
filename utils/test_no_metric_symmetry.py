
def test_no_metric_symmetry():
    # no metric symmetry; A no symmetry
    # A^d1_d0 * A^d0_d1
    # T_c = A^d0_d1 * A^d1_d0
    Lorentz = TensorIndexType('Lorentz', dummy_name='L', metric_symmetry=0)
    d0, d1, d2, d3 = tensor_indices('d:4', Lorentz)
    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.no_symmetry(2))
    t = A(d1, -d0)*A(d0, -d1)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, -L_1)*A(L_1, -L_0)'

    # A^d1_d2 * A^d0_d3 * A^d2_d1 * A^d3_d0
    # T_c = A^d0_d1 * A^d1_d0 * A^d2_d3 * A^d3_d2
    t = A(d1, -d2)*A(d0, -d3)*A(d2, -d1)*A(d3, -d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, -L_1)*A(L_1, -L_0)*A(L_2, -L_3)*A(L_3, -L_2)'

    # A^d0_d2 * A^d1_d3 * A^d3_d0 * A^d2_d1
    # T_c = A^d0_d1 * A^d1_d2 * A^d2_d3 * A^d3_d0
    t = A(d0, -d1)*A(d1, -d2)*A(d2, -d3)*A(d3, -d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, -L_1)*A(L_1, -L_2)*A(L_2, -L_3)*A(L_3, -L_0)'


def test_no_metric_symmetry():
    # no metric symmetry
    # A^d1_d0 * A^d0_d1; ord = [d0,-d0,d1,-d1]; g= [2,1,0,3,4,5]
    # T_c = A^d0_d1 * A^d1_d0; can = [0,3,2,1,4,5]
    g = Permutation([2,1,0,3,4,5])
    can = canonicalize(g, list(range(4)), None, [[], [Permutation(list(range(4)))], 2, 0])
    assert can == [0,3,2,1,4,5]

    # A^d1_d2 * A^d0_d3 * A^d2_d1 * A^d3_d0
    # ord = [d0,-d0,d1,-d1,d2,-d2,d3,-d3]
    #        0    1  2  3  4   5   6   7
    # g = [2,5,0,7,4,3,6,1,8,9]
    # T_c = A^d0_d1 * A^d1_d0 * A^d2_d3 * A^d3_d2
    # can = [0,3,2,1,4,7,6,5,8,9]
    g = Permutation([2,5,0,7,4,3,6,1,8,9])
    #can = canonicalize(g, list(range(8)), 0, [[], [list(range(4))], 4, 0])
    #assert can == [0, 2, 3, 1, 4, 6, 7, 5, 8, 9]
    can = canonicalize(g, list(range(8)), None, [[], [Permutation(list(range(4)))], 4, 0])
    assert can == [0, 3, 2, 1, 4, 7, 6, 5, 8, 9]

    # A^d0_d2 * A^d1_d3 * A^d3_d0 * A^d2_d1
    # g = [0,5,2,7,6,1,4,3,8,9]
    # T_c = A^d0_d1 * A^d1_d2 * A^d2_d3 * A^d3_d0
    # can = [0,3,2,5,4,7,6,1,8,9]
    g = Permutation([0,5,2,7,6,1,4,3,8,9])
    can = canonicalize(g, list(range(8)), None, [[], [Permutation(list(range(4)))], 4, 0])
    assert can == [0,3,2,5,4,7,6,1,8,9]

    g = Permutation([12,7,10,3,14,13,4,11,6,1,2,9,0,15,8,5,16,17])
    can = canonicalize(g, list(range(16)), None, [[], [Permutation(list(range(4)))], 8, 0])
    assert can == [0,3,2,5,4,7,6,1,8,11,10,13,12,15,14,9,16,17]

