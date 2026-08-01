
def test_replace_arrays_partial_derivative():

    x, y, z, t = symbols("x y z t")

    expr = PartialDerivative(A(i), B(j))
    repl = expr.replace_with_arrays({A(i): [sin(x)*cos(y), x**3*y**2], B(i): [x, y]})
    assert repl == Array([[cos(x)*cos(y), -sin(x)*sin(y)], [3*x**2*y**2, 2*x**3*y]])
    repl = expr.replace_with_arrays({A(i): [sin(x)*cos(y), x**3*y**2], B(i): [x, y]}, [-j, i])
    assert repl == Array([[cos(x)*cos(y), 3*x**2*y**2], [-sin(x)*sin(y), 2*x**3*y]])

    # d(A^i)/d(A_j) = d(g^ik A_k)/d(A_j) = g^ik delta_jk
    expr = PartialDerivative(A(i), A(-j))
    assert expr.get_free_indices() == [i, j]
    assert expr.get_indices() == [i, j]
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, 1)}, [i, j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, -1)}, [i, j]) == Array([[1, 0], [0, -1]])
    assert expr.replace_with_arrays({A(-i): [x, y], L: diag(1, 1)}, [i, j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(-i): [x, y], L: diag(1, -1)}, [i, j]) == Array([[1, 0], [0, -1]])

    expr = PartialDerivative(A(i), A(j))
    assert expr.get_free_indices() == [i, -j]
    assert expr.get_indices() == [i, -j]
    assert expr.replace_with_arrays({A(i): [x, y]}, [i, -j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, 1)}, [i, -j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, -1)}, [i, -j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(-i): [x, y], L: diag(1, 1)}, [i, -j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(-i): [x, y], L: diag(1, -1)}, [i, -j]) == Array([[1, 0], [0, 1]])

    expr = PartialDerivative(A(-i), A(-j))
    assert expr.get_free_indices() == [-i, j]
    assert expr.get_indices() == [-i, j]
    assert expr.replace_with_arrays({A(-i): [x, y]}, [-i, j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(-i): [x, y], L: diag(1, 1)}, [-i, j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(-i): [x, y], L: diag(1, -1)}, [-i, j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, 1)}, [-i, j]) == Array([[1, 0], [0, 1]])
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, -1)}, [-i, j]) == Array([[1, 0], [0, 1]])

    expr = PartialDerivative(A(i), A(i))
    assert expr.get_free_indices() == []
    assert expr.get_indices() == [L_0, -L_0]
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, 1)}, []) == 2
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, -1)}, []) == 2

    expr = PartialDerivative(A(-i), A(-i))
    assert expr.get_free_indices() == []
    assert expr.get_indices() == [-L_0, L_0]
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, 1)}, []) == 2
    assert expr.replace_with_arrays({A(i): [x, y], L: diag(1, -1)}, []) == 2

    expr = PartialDerivative(H(i, j) + H(j, i), A(i))
    assert expr.get_indices() == [L_0, j, -L_0]
    assert expr.get_free_indices() == [j]

    expr = PartialDerivative(H(i, j) + H(j, i), A(k))*B(-i)
    assert expr.get_indices() == [L_0, j, -k, -L_0]
    assert expr.get_free_indices() == [j, -k]

    expr = PartialDerivative(A(i)*(H(-i, j) + H(j, -i)), A(j))
    assert expr.get_indices() == [L_0, -L_0, L_1, -L_1]
    assert expr.get_free_indices() == []

    expr = A(j)*A(-j) + expr
    assert expr.get_indices() == [L_0, -L_0, L_1, -L_1]
    assert expr.get_free_indices() == []

    expr = A(i)*(B(j)*PartialDerivative(C(-j), D(i)) + C(j)*PartialDerivative(D(-j), B(i)))
    assert expr.get_indices() == [L_0, L_1, -L_1, -L_0]
    assert expr.get_free_indices() == []

    expr = A(i)*PartialDerivative(C(-j), D(i))
    assert expr.get_indices() == [L_0, -j, -L_0]
    assert expr.get_free_indices() == [-j]

