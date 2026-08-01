
def test_custom_branchbound() -> None:
    np = pytest.importorskip("numpy")

    eq, shapes = rand_equation(8, 4, seed=42)
    views = list(map(np.ones, shapes))
    optimizer = oe.BranchBound(nbranch=2, cutoff_flops_factor=10, minimize="size")

    path, path_info = oe.contract_path(eq, *views, optimize=optimizer)

    assert path == optimizer.path
    assert path_info.largest_intermediate == optimizer.best["size"]
    assert path_info.opt_cost == optimizer.best["flops"]

    # tweak settings and run again
    optimizer.nbranch = 3
    optimizer.cutoff_flops_factor = 4
    path, path_info = oe.contract_path(eq, *views, optimize=optimizer)

    assert path == optimizer.path
    assert path_info.largest_intermediate == optimizer.best["size"]
    assert path_info.opt_cost == optimizer.best["flops"]

    # check error if we try and reuse the optimizer on a different expression
    eq, shapes = rand_equation(8, 4, seed=41)
    views = list(map(np.ones, shapes))
    with pytest.raises(ValueError):
        path, path_info = oe.contract_path(eq, *views, optimize=optimizer)

