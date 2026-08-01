
def test_large_path(num_symbols: int) -> None:
    symbols = "".join(oe.get_symbol(i) for i in range(num_symbols))
    dimension_dict = dict(zip(symbols, itertools.cycle([2, 3, 4])))
    expression = ",".join(symbols[t : t + 2] for t in range(num_symbols - 1))
    tensors = build_shapes(expression, dimension_dict=dimension_dict)

    # Check that path construction does not crash
    oe.contract_path(expression, *tensors, optimize="greedy", shapes=True)

