
def test_torch_special_matrices():
    if not torch:
        skip("PyTorch not installed")

    expr = Identity(3)
    assert torch_code(expr) == "torch.eye(3)"

    n = symbols("n")
    expr = Identity(n)
    assert torch_code(expr) == "torch.eye(n, n)"

    expr = ZeroMatrix(2, 3)
    assert torch_code(expr) == "torch.zeros((2, 3))"

    m, n = symbols("m n")
    expr = ZeroMatrix(m, n)
    assert torch_code(expr) == "torch.zeros((m, n))"

    expr = OneMatrix(2, 3)
    assert torch_code(expr) == "torch.ones((2, 3))"

    expr = OneMatrix(m, n)
    assert torch_code(expr) == "torch.ones((m, n))"

