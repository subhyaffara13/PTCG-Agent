
def test_torch_special_matrices_lambdify():
    if not torch:
        skip("PyTorch not installed")

    expr = Identity(3)
    f = lambdify([], expr, 'torch')
    result = f()
    expected = torch.eye(3)
    assert torch.allclose(result, expected)

    expr = ZeroMatrix(2, 3)
    f = lambdify([], expr, 'torch')
    result = f()
    expected = torch.zeros((2, 3))
    assert torch.allclose(result, expected)

    expr = OneMatrix(2, 3)
    f = lambdify([], expr, 'torch')
    result = f()
    expected = torch.ones((2, 3))
    assert torch.allclose(result, expected)

