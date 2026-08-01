
def test_torch_relational():
    if not torch:
        skip("PyTorch not installed")

    expr = Eq(x, y)
    assert torch_code(expr) == "torch.eq(x, y)"
    _compare_torch_relational((x, y), expr)

    expr = Ne(x, y)
    assert torch_code(expr) == "torch.ne(x, y)"
    _compare_torch_relational((x, y), expr)

    expr = Ge(x, y)
    assert torch_code(expr) == "torch.ge(x, y)"
    _compare_torch_relational((x, y), expr)

    expr = Gt(x, y)
    assert torch_code(expr) == "torch.gt(x, y)"
    _compare_torch_relational((x, y), expr)

    expr = Le(x, y)
    assert torch_code(expr) == "torch.le(x, y)"
    _compare_torch_relational((x, y), expr)

    expr = Lt(x, y)
    assert torch_code(expr) == "torch.lt(x, y)"
    _compare_torch_relational((x, y), expr)

