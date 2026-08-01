
def test_custom_dp_can_set_minimize(minimize: str, cost: int, width: int, path: PathType) -> None:
    eq, shapes = rand_equation(10, 4, seed=43)
    opt = oe.DynamicProgramming(minimize=minimize)
    info = oe.contract_path(eq, *shapes, shapes=True, optimize=opt)[1]
    assert info.path == path
    assert info.opt_cost == cost
    assert info.largest_intermediate == width

