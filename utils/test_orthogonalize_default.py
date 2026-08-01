
def test_orthogonalize_default(func, type, xp):
    # Test orthogonalize is the default when norm="ortho", but not otherwise
    x = xp.asarray(np.random.rand(100))

    for norm, ortho in [
            ("forward", False),
            ("backward", False),
            ("ortho", True),
    ]:
        a = func(x, type=type, norm=norm, orthogonalize=ortho)
        b = func(x, type=type, norm=norm)
        xp_assert_close(a, b)

