import math


def test_torch_derivative_lambdify():
    if not torch:
        skip("PyTorch not installed")

    x = symbols("x")
    y = symbols("y")

    expr = Derivative(x ** 2, x)
    f = lambdify(x, expr, 'torch')
    x_val = torch.tensor(2.0, requires_grad=True)
    result = f(x_val)
    assert torch.isclose(result, torch.tensor(4.0))

    expr = Derivative(sin(x), (x, 2))
    f = lambdify(x, expr, 'torch')
    # Second derivative of sin(x) at x=0 is 0, not -1
    x_val = torch.tensor(0.0, requires_grad=True)
    result = f(x_val)
    assert torch.isclose(result, torch.tensor(0.0), atol=1e-5)

    x_val = torch.tensor(math.pi / 2, requires_grad=True)
    result = f(x_val)
    assert torch.isclose(result, torch.tensor(-1.0), atol=1e-5)

    expr = Derivative(x * y ** 2, x, y)
    f = lambdify((x, y), expr, 'torch')
    x_val = torch.tensor(2.0, requires_grad=True)
    y_val = torch.tensor(3.0, requires_grad=True)
    result = f(x_val, y_val)
    assert torch.isclose(result, torch.tensor(6.0))

