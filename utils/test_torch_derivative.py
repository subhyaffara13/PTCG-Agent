
def test_torch_derivative():
    """Test derivative handling."""
    expr = Derivative(sin(x), x)
    assert torch_code(expr) == 'torch.autograd.grad(torch.sin(x), x)[0]'

