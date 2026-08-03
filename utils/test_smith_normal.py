import random

def test_smith_normal():

    m = DM([
        [12, 6, 4, 8],
        [3, 9, 6, 12],
        [2, 16, 14, 28],
        [20, 10, 10, 20]], ZZ)

    smf = DM([
        [1, 0, 0, 0],
        [0, 10, 0, 0],
        [0, 0, 30, 0],
        [0, 0, 0, 0]], ZZ)

    s = DM([
        [0, 1, -1, 0],
        [1, -4, 0, 0],
        [0, -2, 3, 0],
        [-2, 2, -1, 1]], ZZ)

    t = DM([
        [1, 1, 10, 0],
        [0, -1, -2, 0],
        [0, 1, 3, -2],
        [0, 0, 0, 1]], ZZ)

    assert smith_normal_form(m).to_dense() == smf
    assert smith_normal_decomp(m) == (smf, s, t)
    assert is_smith_normal_form(smf)
    assert smf == s * m * t

    m00 = DomainMatrix.zeros((0, 0), ZZ).to_dense()
    m01 = DomainMatrix.zeros((0, 1), ZZ).to_dense()
    m10 = DomainMatrix.zeros((1, 0), ZZ).to_dense()
    i11 = DM([[1]], ZZ)

    assert smith_normal_form(m00) == m00.to_sparse()
    assert smith_normal_form(m01) == m01.to_sparse()
    assert smith_normal_form(m10) == m10.to_sparse()
    assert smith_normal_form(i11) == i11.to_sparse()

    assert smith_normal_decomp(m00) == (m00, m00, m00)
    assert smith_normal_decomp(m01) == (m01, m00, i11)
    assert smith_normal_decomp(m10) == (m10, i11, m00)
    assert smith_normal_decomp(i11) == (i11, i11, i11)

    x = Symbol('x')
    m = DM([[x-1,  1, -1],
            [  0,  x, -1],
            [  0, -1,  x]], QQ[x])
    dx = m.domain.gens[0]
    assert invariant_factors(m) == (1, dx-1, dx**2-1)

    zr = DomainMatrix([], (0, 2), ZZ)
    zc = DomainMatrix([[], []], (2, 0), ZZ)
    assert smith_normal_form(zr).to_dense() == zr
    assert smith_normal_form(zc).to_dense() == zc

    assert smith_normal_form(DM([[2, 4]], ZZ)).to_dense() == DM([[2, 0]], ZZ)
    assert smith_normal_form(DM([[0, -2]], ZZ)).to_dense() == DM([[2, 0]], ZZ)
    assert smith_normal_form(DM([[0], [-2]], ZZ)).to_dense() == DM([[2], [0]], ZZ)

    assert smith_normal_decomp(DM([[0, -2]], ZZ)) == (
        DM([[2, 0]], ZZ), DM([[-1]], ZZ), DM([[0, 1], [1, 0]], ZZ)
    )
    assert smith_normal_decomp(DM([[0], [-2]], ZZ)) == (
        DM([[2], [0]], ZZ), DM([[0, -1], [1, 0]], ZZ), DM([[1]], ZZ)
    )

    m =   DM([[3, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0]], ZZ)
    snf = DM([[1, 0, 0, 0], [0, 6, 0, 0], [0, 0, 0, 0]], ZZ)
    s = DM([[1, 0, 1], [2, 0, 3], [0, 1, 0]], ZZ)
    t = DM([[1, -2, 0, 0], [0, 0, 0, 1], [-1, 3, 0, 0], [0, 0, 1, 0]], ZZ)

    assert smith_normal_form(m).to_dense() == snf
    assert smith_normal_decomp(m) == (snf, s, t)
    assert is_smith_normal_form(snf)
    assert snf == s * m * t

    raises(ValueError, lambda: smith_normal_form(DM([[1]], ZZ[x])))


def test_smith_normal():
    m = Matrix([[12,6,4,8],[3,9,6,12],[2,16,14,28],[20,10,10,20]])
    smf = Matrix([[1, 0, 0, 0], [0, 10, 0, 0], [0, 0, 30, 0], [0, 0, 0, 0]])
    assert smith_normal_form(m) == smf

    a, s, t = smith_normal_decomp(m)
    assert a == s * m * t

    x = Symbol('x')
    with warns_deprecated_sympy():
        m = Matrix([[Poly(x-1), Poly(1, x),Poly(-1,x)],
                    [0, Poly(x), Poly(-1,x)],
                    [Poly(0,x),Poly(-1,x),Poly(x)]])
    invs = 1, x - 1, x**2 - 1
    assert invariant_factors(m, domain=QQ[x]) == invs

    m = Matrix([[2, 4]])
    smf = Matrix([[2, 0]])
    assert smith_normal_form(m) == smf

    prng = random.Random(0)
    for i in range(6):
        for j in range(6):
            for _ in range(10 if i*j else 1):
                m = randMatrix(i, j, max=5, percent=50, prng=prng)
                a, s, t = smith_normal_decomp(m)
                assert a == s * m * t
                assert is_smith_normal_form(a)
                s.inv().to_DM(ZZ)
                t.inv().to_DM(ZZ)

                a, s, t = smith_normal_decomp(m, QQ)
                assert a == s * m * t
                assert is_smith_normal_form(a)
                s.inv()
                t.inv()

