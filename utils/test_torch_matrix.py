
def test_torch_matrix():
    if torch is None:
        skip("PyTorch not installed")

    expr = M
    assert torch_code(expr) == "M"
    f = lambdify((M,), expr, "torch")
    eye_mat = eye(3)
    eye_tensor = torch.tensor(eye_mat.tolist(), dtype=torch.float64)
    assert torch.allclose(f(eye_tensor), eye_tensor)

    expr = M * N
    assert torch_code(expr) == "torch.matmul(M, N)"
    _compare_torch_matrix((M, N), expr)

    expr = M ** 3
    assert torch_code(expr) == "torch.mm(torch.mm(M, M), M)"
    _compare_torch_matrix((M,), expr)

    expr = M * N * P * Q
    assert torch_code(expr) == "torch.matmul(torch.matmul(torch.matmul(M, N), P), Q)"
    _compare_torch_matrix((M, N, P, Q), expr)

    expr = Trace(M)
    assert torch_code(expr) == "torch.trace(M)"
    _compare_torch_matrix((M,), expr)

    expr = Determinant(M)
    assert torch_code(expr) == "torch.det(M)"
    _compare_torch_matrix((M,), expr)

    expr = HadamardProduct(M, N)
    assert torch_code(expr) == "torch.mul(M, N)"
    _compare_torch_matrix((M, N), expr)

    expr = Inverse(M)
    assert torch_code(expr) == "torch.linalg.inv(M)"

    # For inverse, use a matrix that's guaranteed to be invertible
    eye_mat = eye(3)
    eye_tensor = torch.tensor(eye_mat.tolist(), dtype=torch.float64)
    f = lambdify((M,), expr, "torch")
    result = f(eye_tensor)
    expected = torch.linalg.inv(eye_tensor)
    assert torch.allclose(result, expected)

