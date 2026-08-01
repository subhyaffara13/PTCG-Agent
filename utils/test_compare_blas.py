
def test_compare_blas(optimize: OptimizeKind, string: str) -> None:
    views = build_views(string)

    ein = contract(string, *views, optimize=False)
    opt = contract(string, *views, optimize=optimize)
    assert np.allclose(ein, opt)

