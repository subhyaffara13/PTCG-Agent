
def test_no_sharing_separate_cache(backend: BackendType) -> None:
    eq = "ab,bc,cd->"
    views = build_views(eq)
    expr = contract_expression(eq, *(v.shape for v in views))

    print("-" * 40)
    print("Without sharing:")
    with shared_intermediates() as cache:
        expr(*views, backend=backend)
        expected = count_cached_ops(cache)
        expected.update(count_cached_ops(cache))  # we expect double

    print("-" * 40)
    print("With sharing:")
    with shared_intermediates() as cache1:
        expr(*views, backend=backend)
        actual = count_cached_ops(cache1)
    with shared_intermediates() as cache2:
        expr(*views, backend=backend)
        actual.update(count_cached_ops(cache2))

    print("-" * 40)
    print(f"Without sharing: {expected} expressions")
    print(f"With sharing: {actual} expressions")
    assert actual == expected

