
def test_torch_multi_variable_derivatives():
    if not torch:
        skip("PyTorch not installed")

    x, y, z = symbols("x y z")

    expr = Derivative(sin(x), x)
    assert torch_code(expr) == "torch.autograd.grad(torch.sin(x), x)[0]"

    expr = Derivative(sin(x), (x, 2))
    assert torch_code(
        expr) == "torch.autograd.grad(torch.autograd.grad(torch.sin(x), x, create_graph=True)[0], x, create_graph=True)[0]"

    expr = Derivative(sin(x * y), x, y)
    result = torch_code(expr)
    expected = "torch.autograd.grad(torch.autograd.grad(torch.sin(x*y), x, create_graph=True)[0], y, create_graph=True)[0]"
    normalized_result = result.replace(" ", "")
    normalized_expected = expected.replace(" ", "")
    assert normalized_result == normalized_expected

    expr = Derivative(sin(x), x, x)
    result = torch_code(expr)
    expected = "torch.autograd.grad(torch.autograd.grad(torch.sin(x), x, create_graph=True)[0], x, create_graph=True)[0]"
    assert result == expected

    expr = Derivative(sin(x * y * z), x, (y, 2), z)
    result = torch_code(expr)
    expected = "torch.autograd.grad(torch.autograd.grad(torch.autograd.grad(torch.autograd.grad(torch.sin(x*y*z), x, create_graph=True)[0], y, create_graph=True)[0], y, create_graph=True)[0], z, create_graph=True)[0]"
    normalized_result = result.replace(" ", "")
    normalized_expected = expected.replace(" ", "")
    assert normalized_result == normalized_expected

