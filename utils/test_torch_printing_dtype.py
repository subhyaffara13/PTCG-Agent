
def test_torch_printing_dtype():
    if not torch:
        skip("PyTorch not installed")

    # matrix printing with default dtype
    expr = Matrix([[x, sin(y)], [exp(z), -t]])
    assert "dtype=torch.float64" in torch_code(expr)

    # explicit dtype
    assert "dtype=torch.float32" in torch_code(expr, dtype="torch.float32")

    # with requires_grad
    result = torch_code(expr, requires_grad=True)
    assert "requires_grad=True" in result
    assert "dtype=torch.float64" in result

    # both
    result = torch_code(expr, requires_grad=True, dtype="torch.float32")
    assert "requires_grad=True" in result
    assert "dtype=torch.float32" in result

