
def test_sharing_value(eq: str, backend: BackendType) -> None:
    views = build_views(eq)
    shapes = [v.shape for v in views]
    expr = contract_expression(eq, *shapes)

    expected = expr(*views, backend=backend)
    with shared_intermediates():
        actual = expr(*views, backend=backend)

    assert (actual == expected).all()

