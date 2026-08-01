
def test_sharing_reused_cache(backend: BackendType) -> None:
    eq = "ab,bc,cd->"
    views = build_views(eq)
    expr = contract_expression(eq, *(v.shape for v in views))

    print("-" * 40)
    print("Without sharing:")
    with shared_intermediates() as cache:
        expr(*views, backend=backend)
        expected = count_cached_ops(cache)

    print("-" * 40)
    print("With sharing:")
    with shared_intermediates() as cache:
        expr(*views, backend=backend)
    with shared_intermediates(cache):
        expr(*views, backend=backend)
        actual = count_cached_ops(cache)

    print("-" * 40)
    print(f"Without sharing: {expected} expressions")
    print(f"With sharing: {actual} expressions")
    assert actual == expected

