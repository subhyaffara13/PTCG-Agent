
def test_chain():
    rl = chain(posdec, posdec)
    assert rl(5) == 3
    assert rl(1) == 0


def test_chain():
    assert list(chain()(2)) == [2]  # identity
    assert list(chain(inc, inc)(2)) == [4]
    assert list(chain(branch5, inc)(4)) == [4]
    assert set(chain(branch5, inc)(5)) == {5, 7}
    assert list(chain(inc, branch5)(5)) == [7]


def test_chain(size: int, backend: BackendType) -> None:
    xs = [np.random.rand(2, 2) for _ in range(size)]
    shapes = [x.shape for x in xs]
    alphabet = "".join(get_symbol(i) for i in range(size + 1))
    names = [alphabet[i : i + 2] for i in range(size)]
    inputs = ",".join(names)

    with shared_intermediates():
        print(inputs)
        for i in range(size + 1):
            target = alphabet[i]
            eq = f"{inputs}->{target}"
            path_info = contract_path(eq, *xs)
            print(path_info[1])
            expr = contract_expression(eq, *shapes)
            expr(*xs, backend=backend)
        print("-" * 40)

