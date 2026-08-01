
def test_mul_noncommutative_pow():
    A, B, C = symbols('A B C', commutative=False)
    w = symbols('w', cls=Wild, commutative=False)

    assert (A*B*w).matches(A*B**2) == {w: B}
    assert (A*(B**2)*w*(B**3)).matches(A*B**8) == {w: B**3}
    assert (A*B*w*C).matches(A*(B**4)*C) == {w: B**3}

    assert (A*B*(w**(-1))).matches(A*B*(C**(-1))) == {w: C}
    assert (A*(B*w)**(-1)*C).matches(A*(B*C)**(-1)*C) == {w: C}

    assert ((w**2)*B*C).matches((A**2)*B*C) == {w: A}
    assert ((w**2)*B*(w**3)).matches((A**2)*B*(A**3)) == {w: A}
    assert ((w**2)*B*(w**4)).matches((A**2)*B*(A**2)) is None

