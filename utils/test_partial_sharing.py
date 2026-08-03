from typing import Any

def test_partial_sharing(backend: BackendType) -> None:
    eq = "ab,bc,de->"
    x, y, z1 = build_views(eq)  # type: ignore
    z2 = 2.0 * z1 - 1.0
    expr = contract_expression(eq, x.shape, y.shape, z1.shape)

    print("-" * 40)
    print("Without sharing:")
    num_exprs_nosharing: Any = Counter()
    with shared_intermediates() as cache:
        expr(x, y, z1, backend=backend)
        num_exprs_nosharing.update(count_cached_ops(cache))
    with shared_intermediates() as cache:
        expr(x, y, z2, backend=backend)
        num_exprs_nosharing.update(count_cached_ops(cache))

    print("-" * 40)
    print("With sharing:")
    with shared_intermediates() as cache:
        expr(x, y, z1, backend=backend)
        expr(x, y, z2, backend=backend)
        num_exprs_sharing = count_cached_ops(cache)

    print("-" * 40)
    print(f"Without sharing: {num_exprs_nosharing} expressions")
    print(f"With sharing: {num_exprs_sharing} expressions")
    assert num_exprs_nosharing["einsum"] > num_exprs_sharing["einsum"]

