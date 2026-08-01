
def test_path_with_assumed_shapes() -> None:
    path, _ = oe.contract_path("ab,bc,cd", [[5, 3]], [[2], [4]], [[3, 2]])
    assert path == [(0, 1), (0, 1)]

