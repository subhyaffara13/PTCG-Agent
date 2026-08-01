
def test_contract_plain_types(optimize: OptimizeKind) -> None:
    expr = "ij,jk,kl->il"
    ops = [np.random.rand(2, 2), np.random.rand(2, 2), np.random.rand(2, 2)]

    path = contract_path(expr, *ops, optimize=optimize)
    assert len(path) == 2

    result = contract(expr, *ops, optimize=optimize)
    assert result.shape == (2, 2)

