
def test_dp_edge_cases_all_singlet_indices() -> None:
    eq = "a,bcd,efg->"
    shapes = [(2,), (2, 2, 2), (2, 2, 2)]
    info = oe.contract_path(eq, *shapes, shapes=True, optimize="dp")[1]
    assert max(info.scale_list) == 3

