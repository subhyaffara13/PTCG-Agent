
def test_compare_greek(optimize: OptimizeKind, string: str) -> None:
    views = build_views(string)

    ein = contract(string, *views, optimize=False, use_blas=False)

    # convert to greek
    string = "".join(chr(ord(c) + 848) if c not in ",->." else c for c in string)

    opt = contract(string, *views, optimize=optimize, use_blas=False)
    assert np.allclose(ein, opt)

