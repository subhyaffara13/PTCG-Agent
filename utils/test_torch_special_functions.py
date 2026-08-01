
def test_torch_special_functions():
    if not torch:
        skip("PyTorch not installed")

    expr = Heaviside(x)
    assert torch_code(expr) == "torch.heaviside(x, 1/2)"

    expr = Heaviside(x, 0)
    assert torch_code(expr) == "torch.heaviside(x, 0)"

    expr = gamma(x)
    assert torch_code(expr) == "torch.special.gamma(x)"

    expr = polygamma(0, x)  # Use polygamma instead of digamma because sympy will default to that anyway
    assert torch_code(expr) == "torch.special.digamma(x)"

    expr = gamma(sin(x))
    assert torch_code(expr) == "torch.special.gamma(torch.sin(x))"

