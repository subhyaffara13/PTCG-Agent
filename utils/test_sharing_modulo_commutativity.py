
def test_sharing_modulo_commutativity(eq: str, backend: BackendType) -> None:
    ops = tuple(to_backend[backend](x) for x in build_views(eq))
    inputs, output, _ = parse_einsum_input([eq] + list(ops))
    inputs_list = inputs.split(",")

    print("-" * 40)
    print("Without sharing:")
    with shared_intermediates() as cache:
        _einsum(eq, *ops, backend=backend)
        expected = count_cached_ops(cache)

    print("-" * 40)
    print("With sharing:")
    with shared_intermediates() as cache:
        for permuted in itertools.permutations(zip(inputs_list, ops)):
            permuted_inputs = [p[0] for p in permuted]
            permuted_ops = [p[1] for p in permuted]
            permuted_eq = "{}->{}".format(",".join(permuted_inputs), output)
            _einsum(permuted_eq, *permuted_ops, backend=backend)
        actual = count_cached_ops(cache)

    print("-" * 40)
    print(f"Without sharing: {expected} expressions")
    print(f"With sharing: {actual} expressions")
    assert actual == expected

