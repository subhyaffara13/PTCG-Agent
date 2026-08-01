
def test_dp_errors_when_no_contractions_found() -> None:
    eq, shapes = rand_equation(10, 3, seed=42)

    # first get the actual minimum cost
    opt = oe.DynamicProgramming(minimize="size")
    _, info = oe.contract_path(eq, *shapes, shapes=True, optimize=opt)
    mincost = info.largest_intermediate

    # check we can still find it without minimizing size explicitly
    oe.contract_path(eq, *shapes, shapes=True, memory_limit=mincost, optimize="dp")

    # but check just below this threshold raises
    with pytest.raises(RuntimeError):
        oe.contract_path(eq, *shapes, shapes=True, memory_limit=mincost - 1, optimize="dp")

