
def test_Identity():
    from sympy.matrices.expressions.special import Identity
    assert latex(Identity(1), mat_symbol_style='plain') == r"\mathbb{I}"
    assert latex(Identity(1), mat_symbol_style='bold') == r"\mathbf{I}"


def test_Identity():
    n, m = symbols('n m', integer=True)
    A = MatrixSymbol('A', n, m)
    i, j = symbols('i j')

    In = Identity(n)
    Im = Identity(m)

    assert A*Im == A
    assert In*A == A

    assert In.transpose() == In
    assert In.inverse() == In
    assert In.conjugate() == In
    assert In.adjoint() == In
    assert re(In) == In
    assert im(In) == ZeroMatrix(n, n)

    assert In[i, j] != 0
    assert Sum(In[i, j], (i, 0, n-1), (j, 0, n-1)).subs(n,3).doit() == 3
    assert Sum(Sum(In[i, j], (i, 0, n-1)), (j, 0, n-1)).subs(n,3).doit() == 3

    # If range exceeds the limit `(0, n-1)`, do not remove `Piecewise`:
    expr = Sum(In[i, j], (i, 0, n-1))
    assert expr.doit() == 1
    expr = Sum(In[i, j], (i, 0, n-2))
    assert expr.doit().dummy_eq(
        Piecewise(
            (1, (j >= 0) & (j <= n-2)),
            (0, True)
        )
    )
    expr = Sum(In[i, j], (i, 1, n-1))
    assert expr.doit().dummy_eq(
        Piecewise(
            (1, (j >= 1) & (j <= n-1)),
            (0, True)
        )
    )
    assert Identity(3).as_explicit() == ImmutableDenseMatrix.eye(3)

