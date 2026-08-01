
def test_commutator():
    c = Comm(A, B)
    assert c.is_commutative is False
    assert isinstance(c, Comm)
    assert c.subs(A, C) == Comm(C, B)


def test_commutator():
    A = Operator('A')
    B = Operator('B')
    c = Commutator(A, B)
    c_tall = Commutator(A**2, B)
    assert str(c) == '[A,B]'
    assert pretty(c) == '[A,B]'
    assert upretty(c) == '[A,B]'
    assert latex(c) == r'\left[A,B\right]'
    sT(c, "Commutator(Operator(Symbol('A')),Operator(Symbol('B')))")
    assert str(c_tall) == '[A**2,B]'
    ascii_str = \
"""\
[ 2  ]\n\
[A ,B]\
"""
    ucode_str = \
"""\
⎡ 2  ⎤\n\
⎣A ,B⎦\
"""
    assert pretty(c_tall) == ascii_str
    assert upretty(c_tall) == ucode_str
    assert latex(c_tall) == r'\left[A^{2},B\right]'
    sT(c_tall, "Commutator(Pow(Operator(Symbol('A')), Integer(2)),Operator(Symbol('B')))")


def test_commutator():
    assert qapply(Commutator(Jx, Jy)*Jz*po) == I*hbar**3*po
    assert qapply(Commutator(J2, Jz)*Jz*po) == 0
    assert qapply(Commutator(Jz, Foo('F'))*po) == 0
    assert qapply(Commutator(Foo('F'), Jz)*po) == 0


def test_commutator():
    assert Commutator(R2.e_x, R2.e_y) == 0
    assert Commutator(R2.x*R2.e_x, R2.x*R2.e_x) == 0
    assert Commutator(R2.x*R2.e_x, R2.x*R2.e_y) == R2.x*R2.e_y
    c = Commutator(R2.e_x, R2.e_r)
    assert c(R2.x) == R2.y*(R2.x**2 + R2.y**2)**(-1)*sin(R2.theta)


def test_commutator():
    # the commutator of the trivial group and the trivial group is trivial
    S = SymmetricGroup(3)
    triv = PermutationGroup([Permutation([0, 1, 2])])
    assert S.commutator(triv, triv).is_subgroup(triv)
    # the commutator of the trivial group and any other group is again trivial
    A = AlternatingGroup(3)
    assert S.commutator(triv, A).is_subgroup(triv)
    # the commutator is commutative
    for i in (3, 4, 5):
        S = SymmetricGroup(i)
        A = AlternatingGroup(i)
        D = DihedralGroup(i)
        assert S.commutator(A, D).is_subgroup(S.commutator(D, A))
    # the commutator of an abelian group is trivial
    S = SymmetricGroup(7)
    A1 = AbelianGroup(2, 5)
    A2 = AbelianGroup(3, 4)
    triv = PermutationGroup([Permutation([0, 1, 2, 3, 4, 5, 6])])
    assert S.commutator(A1, A1).is_subgroup(triv)
    assert S.commutator(A2, A2).is_subgroup(triv)
    # examples calculated by hand
    S = SymmetricGroup(3)
    A = AlternatingGroup(3)
    assert S.commutator(A, S).is_subgroup(A)

