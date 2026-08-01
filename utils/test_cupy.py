
def test_cupy(string: str) -> None:
    np = pytest.importorskip("numpy")  # pragma: no cover
    cupy = pytest.importorskip("cupy")

    views = build_views(string)
    ein = contract(string, *views, optimize=False, use_blas=False)
    shps = [v.shape for v in views]

    expr = contract_expression(string, *shps, optimize=True)

    opt = expr(*views, backend="cupy")
    assert np.allclose(ein, opt)

    # test non-conversion mode
    cupy_views = [backends.to_cupy(view) for view in views]
    cupy_opt = expr(*cupy_views)
    assert isinstance(cupy_opt, cupy.ndarray)
    assert np.allclose(ein, cupy.asnumpy(cupy_opt))

