
def test_tensor_expand():
    L = TensorIndexType("L")

    i, j, k = tensor_indices("i j k", L)
    L_0 = TensorIndex("L_0", L)

    A, B, C, D = tensor_heads("A B C D", [L])

    F = Function("F")
    x = Symbol("x")

    assert isinstance(Add(A(i), B(i)), TensAdd)
    assert isinstance(expand(A(i)+B(i)), TensAdd)

    expr = A(i)*(A(-i)+B(-i))
    assert expr.args == (A(L_0), A(-L_0) + B(-L_0))
    assert expr != A(i)*A(-i) + A(i)*B(-i)
    assert expr.expand() == A(i)*A(-i) + A(i)*B(-i)
    assert str(expr) == "A(L_0)*(A(-L_0) + B(-L_0))"

    expr = A(i)*A(j) + A(i)*B(j)
    assert str(expr) == "A(i)*A(j) + A(i)*B(j)"

    expr = A(-i)*(A(i)*A(j) + A(i)*B(j)*C(k)*C(-k))
    assert expr != A(-i)*A(i)*A(j) + A(-i)*A(i)*B(j)*C(k)*C(-k)
    assert expr.expand() == A(-i)*A(i)*A(j) + A(-i)*A(i)*B(j)*C(k)*C(-k)
    assert str(expr) == "A(-L_0)*(A(L_0)*A(j) + A(L_0)*B(j)*C(L_1)*C(-L_1))"
    assert str(expr.canon_bp()) == 'A(j)*A(L_0)*A(-L_0) + A(L_0)*A(-L_0)*B(j)*C(L_1)*C(-L_1)'

    expr = A(-i)*(2*A(i)*A(j) + A(i)*B(j))
    assert expr.expand() == 2*A(-i)*A(i)*A(j) + A(-i)*A(i)*B(j)

    expr = 2*A(i)*A(-i)
    assert expr.coeff == 2

    expr = A(i)*(B(j)*C(k) + C(j)*(A(k) + D(k)))
    assert str(expr) == "A(i)*(B(j)*C(k) + C(j)*(A(k) + D(k)))"
    assert str(expr.expand()) == "A(i)*B(j)*C(k) + A(i)*C(j)*A(k) + A(i)*C(j)*D(k)"

    assert isinstance(TensMul(3), TensMul)
    tm = TensMul(3).doit()
    assert tm == 3
    assert isinstance(tm, Integer)

    p1 = B(j)*B(-j) + B(j)*C(-j)
    p2 = C(-i)*p1
    p3 = A(i)*p2
    assert p3.expand() == A(i)*C(-i)*B(j)*B(-j) + A(i)*C(-i)*B(j)*C(-j)

    expr = A(i)*(B(-i) + C(-i)*(B(j)*B(-j) + B(j)*C(-j)))
    assert expr.expand() == A(i)*B(-i) + A(i)*C(-i)*B(j)*B(-j) + A(i)*C(-i)*B(j)*C(-j)

    expr = C(-i)*(B(j)*B(-j) + B(j)*C(-j))
    assert expr.expand() == C(-i)*B(j)*B(-j) + C(-i)*B(j)*C(-j)

    """
    Test whether expand correctly handles the case where the coeff of a TensMul
    is an add. We do not directly check expr_expand == 2*A(i) + F(x)*A(i) since
    __add__ currently consolidates the coefficients automatically
    """
    expr = (2 + F(x))*A(i)
    expr_expand = expr.expand()
    assert isinstance(expr_expand, TensAdd)
    assert expr_expand.args == (2*A(i), F(x)*A(i))

    expr = (2 + F(x))*A(i) + B(i)
    expr_expand = expr.expand()
    assert isinstance(expr_expand, TensAdd)
    assert expr_expand.args == (2*A(i), F(x)*A(i), B(i))

