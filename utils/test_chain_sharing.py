
def test_chain_sharing(size: int, backend: BackendType) -> None:
    xs = [np.random.rand(2, 2) for _ in range(size)]
    alphabet = "".join(get_symbol(i) for i in range(size + 1))
    names = [alphabet[i : i + 2] for i in range(size)]
    inputs = ",".join(names)

    num_exprs_nosharing = 0
    for i in range(size + 1):
        with shared_intermediates() as cache:
            target = alphabet[i]
            eq = f"{inputs}->{target}"
            expr = contract_expression(eq, *tuple(x.shape for x in xs))
            expr(*xs, backend=backend)
            num_exprs_nosharing += _compute_cost(cache)

    with shared_intermediates() as cache:
        print(inputs)
        for i in range(size + 1):
            target = alphabet[i]
            eq = f"{inputs}->{target}"
            path_info = contract_path(eq, *xs)
            print(path_info[1])
            expr = contract_expression(eq, *[x.shape for x in xs])
            expr(*xs, backend=backend)
        num_exprs_sharing = _compute_cost(cache)

    print("-" * 40)
    print(f"Without sharing: {num_exprs_nosharing} expressions")
    print(f"With sharing: {num_exprs_sharing} expressions")
    assert num_exprs_nosharing > num_exprs_sharing

