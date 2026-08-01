
def test_chain_2_growth(backend: BackendType) -> None:
    sizes = list(range(1, 21))
    costs = []
    for size in sizes:
        xs = [np.random.rand(2, 2) for _ in range(size)]
        alphabet = "".join(get_symbol(i) for i in range(size + 1))
        names = [alphabet[i : i + 2] for i in range(size)]
        inputs = ",".join(names)

        with shared_intermediates() as cache:
            for i in range(size):
                target = alphabet[i : i + 2]
                eq = f"{inputs}->{target}"
                expr = contract_expression(eq, *(x.shape for x in xs))
                expr(*xs, backend=backend)
            costs.append(_compute_cost(cache))

    print(f"sizes = {repr(sizes)}")
    print(f"costs = {repr(costs)}")
    for size, cost in zip(sizes, costs):
        print(f"{size}\t{cost}")

