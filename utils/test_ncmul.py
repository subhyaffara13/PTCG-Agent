
def test_ncmul():
    A = Symbol("A", commutative=False)
    B = Symbol("B", commutative=False)
    C = Symbol("C", commutative=False)
    assert A*B != B*A
    assert A*B*C != C*B*A
    assert A*b*B*3*C == 3*b*A*B*C
    assert A*b*B*3*C != 3*b*B*A*C
    assert A*b*B*3*C == 3*A*B*C*b

    assert A + B == B + A
    assert (A + B)*C != C*(A + B)

    assert C*(A + B)*C != C*C*(A + B)

    assert A*A == A**2
    assert (A + B)*(A + B) == (A + B)**2

    assert A**-1 * A == 1
    assert A/A == 1
    assert A/(A**2) == 1/A

    assert A/(1 + A) == A/(1 + A)

    assert set((A + B + 2*(A + B)).args) == \
        {A, B, 2*(A + B)}

