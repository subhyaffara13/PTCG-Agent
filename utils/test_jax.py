
def test_jax(string: str) -> None:
    np = pytest.importorskip("numpy")  # pragma: no cover
    pytest.importorskip("jax")

    views = build_views(string)
    ein = contract(string, *views, optimize=False, use_blas=False)
    shps = [v.shape for v in views]

    expr = contract_expression(string, *shps, optimize=True)

    opt = expr(*views, backend="jax")
    assert np.allclose(ein, opt)
    assert isinstance(opt, np.ndarray)

