
def test_chain_2(size: int, backend: BackendType) -> None:
    xs = [np.random.rand(2, 2) for _ in range(size)]
    shapes = [x.shape for x in xs]
    alphabet = "".join(get_symbol(i) for i in range(size + 1))
    names = [alphabet[i : i + 2] for i in range(size)]
    inputs = ",".join(names)

    with shared_intermediates():
        print(inputs)
        for i in range(size):
            target = alphabet[i : i + 2]
            eq = f"{inputs}->{target}"
            path_info = contract_path(eq, *xs)
            print(path_info[1])
            expr = contract_expression(eq, *shapes)
            expr(*xs, backend=backend)
        print("-" * 40)

