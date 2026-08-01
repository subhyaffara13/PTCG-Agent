
def test_linear_vs_ssa(equation: str) -> None:
    views = build_views(equation)
    linear_path, _ = contract_path(equation, *views)
    ssa_path = linear_to_ssa(linear_path)
    linear_path2 = ssa_to_linear(ssa_path)
    assert linear_path2 == linear_path

