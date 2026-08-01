
def test_drop_in_replacement(string: str) -> None:
    views = build_views(string)
    opt = contract(string, *views)
    assert np.allclose(opt, np.einsum(string, *views))

