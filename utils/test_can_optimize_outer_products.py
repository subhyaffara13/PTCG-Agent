
def test_can_optimize_outer_products(optimize: OptimizeKind) -> None:
    a, b, c = ((10, 10) for _ in range(3))
    d = (10, 2)

    assert oe.contract_path("ab,cd,ef,fg", a, b, c, d, optimize=optimize, shapes=True)[0] == [
        (2, 3),
        (0, 2),
        (0, 1),
    ]

