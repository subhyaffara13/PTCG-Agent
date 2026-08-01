
def test_requires_grad():
    if not torch:
        skip("PyTorch not installed")

    expr = sin(x) + cos(y)
    f = lambdify([x, y], expr, 'torch')

    # make sure the gradients flow
    x_val = torch.tensor(1.0, requires_grad=True)
    y_val = torch.tensor(2.0, requires_grad=True)
    result = f(x_val, y_val)
    assert result.requires_grad
    result.backward()

    # x_val.grad should be cos(x_val) which is close to cos(1.0)
    assert abs(x_val.grad.item() - float(cos(1.0).evalf())) < 1e-6

    # y_val.grad should be -sin(y_val) which is close to -sin(2.0)
    assert abs(y_val.grad.item() - float(-sin(2.0).evalf())) < 1e-6

