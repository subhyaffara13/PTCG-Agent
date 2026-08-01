
def test_tensorflow(string: str) -> None:
    np = pytest.importorskip("numpy")
    pytest.importorskip("tensorflow")

    views = build_views(string)
    ein = contract(string, *views, optimize=False, use_blas=False)
    opt = np.empty_like(ein)

    shps = [v.shape for v in views]
    expr = contract_expression(string, *shps, optimize=True)

    sess = TFSession(config=_TF_CONFIG)
    with sess.as_default():
        expr(*views, backend="tensorflow", out=opt)
    sess.close()

    assert np.allclose(ein, opt)

    # test non-conversion mode
    tensorflow_views = [backends.to_tensorflow(view) for view in views]
    expr(*tensorflow_views)

