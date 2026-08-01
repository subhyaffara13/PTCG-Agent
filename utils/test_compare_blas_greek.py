
def test_compare_blas_greek(optimize: OptimizeKind, string: str) -> None:
    views = build_views(string)

    ein = contract(string, *views, optimize=False)

    # convert to greek
    string = "".join(chr(ord(c) + 848) if c not in ",->." else c for c in string)

    opt = contract(string, *views, optimize=optimize)
    assert np.allclose(ein, opt)

