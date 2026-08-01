
def test_torch_math():
    if not torch:
        skip("PyTorch not installed")

    expr = Abs(x)
    assert torch_code(expr) == "torch.abs(x)"
    f = lambdify(x, expr, 'torch')
    ma = torch.tensor([[-1, 2, -3, -4]], dtype=torch.float64)
    y_abs = f(ma)
    c = torch.abs(ma)
    assert torch.all(y_abs == c)

    expr = sign(x)
    assert torch_code(expr) == "torch.sign(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-10, 10))

    expr = ceiling(x)
    assert torch_code(expr) == "torch.ceil(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.random())

    expr = floor(x)
    assert torch_code(expr) == "torch.floor(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.random())

    expr = exp(x)
    assert torch_code(expr) == "torch.exp(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-2, 2))

    expr = sqrt(x)
    assert torch_code(expr) == "torch.sqrt(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.random())

    expr = x ** 4
    assert torch_code(expr) == "torch.pow(x, 4)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.random())

    expr = cos(x)
    assert torch_code(expr) == "torch.cos(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.random())

    expr = acos(x)
    assert torch_code(expr) == "torch.acos(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-0.99, 0.99))

    expr = sin(x)
    assert torch_code(expr) == "torch.sin(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.random())

    expr = asin(x)
    assert torch_code(expr) == "torch.asin(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-0.99, 0.99))

    expr = tan(x)
    assert torch_code(expr) == "torch.tan(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-1.5, 1.5))

    expr = atan(x)
    assert torch_code(expr) == "torch.atan(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-5, 5))

    expr = atan2(y, x)
    assert torch_code(expr) == "torch.atan2(y, x)"
    _compare_torch_scalar((y, x), expr, rng=lambda: random.uniform(-5, 5))

    expr = cosh(x)
    assert torch_code(expr) == "torch.cosh(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-2, 2))

    expr = acosh(x)
    assert torch_code(expr) == "torch.acosh(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(1.1, 5))

    expr = sinh(x)
    assert torch_code(expr) == "torch.sinh(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-2, 2))

    expr = asinh(x)
    assert torch_code(expr) == "torch.asinh(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-5, 5))

    expr = tanh(x)
    assert torch_code(expr) == "torch.tanh(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-2, 2))

    expr = atanh(x)
    assert torch_code(expr) == "torch.atanh(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-0.9, 0.9))

    expr = erf(x)
    assert torch_code(expr) == "torch.erf(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(-2, 2))

    expr = loggamma(x)
    assert torch_code(expr) == "torch.lgamma(x)"
    _compare_torch_scalar((x,), expr, rng=lambda: random.uniform(0.5, 5))

