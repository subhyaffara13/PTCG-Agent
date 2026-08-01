
def test_optimal_edge_cases() -> None:
    # Edge test5
    expression = "a,ac,ab,ad,cd,bd,bc->"
    edge_test4 = build_shapes(expression, dimension_dict={"a": 20, "b": 20, "c": 20, "d": 20})
    path, _ = oe.contract_path(expression, *edge_test4, optimize="greedy", memory_limit="max_input", shapes=True)
    assert check_path(path, [(0, 1), (0, 1, 2, 3, 4, 5)])

    path, _ = oe.contract_path(expression, *edge_test4, optimize="optimal", memory_limit="max_input", shapes=True)
    assert check_path(path, [(0, 1), (0, 1, 2, 3, 4, 5)])

