
def test_path_scalar_cases(alg: OptimizeKind, expression: str, order: PathType) -> None:
    views = build_shapes(expression)

    # Test tiny memory limit
    path_ret = oe.contract_path(expression, *views, optimize=alg, shapes=True)
    # print(path_ret[0])
    assert len(path_ret[0]) == order

