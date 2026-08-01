
def test_rand_equation(optimize: OptimizeKind, n: int, reg: int, n_out: int, global_dim: bool) -> None:
    eq, _, size_dict = rand_equation(n, reg, n_out, d_min=2, d_max=5, seed=42, return_size_dict=True)
    views = build_views(eq, size_dict)

    expected = contract(eq, *views, optimize=False)
    actual = contract(eq, *views, optimize=optimize)

    assert np.allclose(expected, actual)

