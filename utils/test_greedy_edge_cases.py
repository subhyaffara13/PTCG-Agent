
def test_greedy_edge_cases() -> None:
    expression = "abc,cfd,dbe,efa"
    dim_dict = {k: 20 for k in expression.replace(",", "")}
    tensors = build_shapes(expression, dimension_dict=dim_dict)

    path, _ = oe.contract_path(expression, *tensors, optimize="greedy", memory_limit="max_input", shapes=True)
    assert check_path(path, [(0, 1, 2, 3)])

    path, _ = oe.contract_path(expression, *tensors, optimize="greedy", memory_limit=-1, shapes=True)
    assert check_path(path, [(0, 1), (0, 2), (0, 1)])

