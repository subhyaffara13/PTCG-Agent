
def test_compare(optimize: OptimizeKind, string: str) -> None:
    views = build_views(string)

    ein = contract(string, *views, optimize=False, use_blas=False)
    opt = contract(string, *views, optimize=optimize, use_blas=False)
    assert np.allclose(ein, opt)


def test_compare(string: str) -> None:
    views = build_views(string)

    ein = contract(string, *views, optimize=False)
    opt = contract(string, *views)
    assert np.allclose(ein, opt)

    opt = contract(string, *views, optimize="optimal")
    assert np.allclose(ein, opt)

